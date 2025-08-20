# utils/drugs.py

import requests
import pandas as pd
from typing import Optional, Dict, Any

# ---------- Common ----------
DEFAULT_HEADERS = {
    "User-Agent": "DrugFetcher/1.0 (+github.com/yourrepo)",
    "Accept": "application/json",
}

OT_GQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"

FALLBACK_DRUGS = {
    "BRCA1": [
        {"Drug": "Olaparib", "ID": "CHEMBL521686", "Mechanism": "PARP inhibitor", "Approval": "FDA approved", "Source": "DrugBank-curated"},
        {"Drug": "Rucaparib", "ID": "CHEMBL1173055", "Mechanism": "PARP inhibitor", "Approval": "FDA accelerated approval", "Source": "DrugBank-curated"},
        {"Drug": "Talazoparib", "ID": "CHEMBL1743089", "Mechanism": "PARP inhibitor", "Approval": "FDA approved", "Source": "DrugBank-curated"},
    ],
    "BRCA2": [
        {"Drug": "Olaparib", "ID": "CHEMBL521686", "Mechanism": "PARP inhibitor", "Approval": "FDA approved", "Source": "DrugBank-curated"},
        {"Drug": "Niraparib", "ID": "CHEMBL2103888", "Mechanism": "PARP inhibitor", "Approval": "FDA approved", "Source": "DrugBank-curated"},
    ],
}
def _safe_json(resp: requests.Response) -> Optional[Dict[str, Any]]:
    try:
        return resp.json()
    except Exception:
        return None


# ---------- ChEMBL ----------
def fetch_from_chembl(gene_symbol: str) -> pd.DataFrame:
    """
    Get drugs targeting a gene via ChEMBL.
    Matches exact gene symbol in synonyms if possible.
    """
    base_url = "https://www.ebi.ac.uk/chembl/api/data"
    try:
        # Step 1: search targets
        search_url = f"{base_url}/target/search.json?q={gene_symbol}"
        r = requests.get(search_url, timeout=15, headers=DEFAULT_HEADERS)
        r.raise_for_status()
        data = r.json()

        targets = data.get("targets", [])
        if not targets:
            print(f"[ChEMBL] No targets returned for {gene_symbol}")
            return pd.DataFrame()

        target_chembl_id = None

        # First try exact match in synonyms
        for tgt in targets:
            for comp in tgt.get("target_components", []):
                for syn in comp.get("target_component_synonyms", []):
                    if syn.get("component_synonym", "").upper() == gene_symbol.upper():
                        target_chembl_id = tgt.get("target_chembl_id")
                        break
                if target_chembl_id:
                    break
            if target_chembl_id:
                break

        # Fallback: pick first target
        if not target_chembl_id:
            target_chembl_id = targets[0].get("target_chembl_id")

        if not target_chembl_id:
            return pd.DataFrame()

        # Step 2: mechanisms
        mech_url = f"{base_url}/mechanism.json?target_chembl_id={target_chembl_id}"
        r2 = requests.get(mech_url, timeout=15, headers=DEFAULT_HEADERS)
        r2.raise_for_status()
        mechs = r2.json().get("mechanisms", [])

        rows = []
        for m in mechs:
            max_phase = m.get("max_phase")
            phase_str = str(int(max_phase)) if isinstance(max_phase, (int, float)) else (
                str(max_phase) if max_phase is not None else "Unknown"
            )
            rows.append({
                "Drug": m.get("molecule_name", ""),
                "ID": f"[{m.get('molecule_chembl_id', '')}](https://www.ebi.ac.uk/chembl/compound_report_card/{m.get('molecule_chembl_id', '')}/)",
                "Mechanism": m.get("mechanism_of_action", "N/A"),
                "Approval": phase_str,
                "Source": "ChEMBL",
            })

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"[ChEMBL] Error fetching for {gene_symbol}: {e}")
        return pd.DataFrame()

def fetch_from_dgidb(gene_symbol: str) -> pd.DataFrame:
    url = f"https://dgidb.org/api/v3/interactions.json?genes={gene_symbol}"
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        rows = []
        for match in data.get("matchedTerms", []):
            for interaction in match.get("interactions", []):
                drug_name = interaction.get("drugName", "")
                chembl_id = interaction.get("drugChemblId", "")
                interaction_types = interaction.get("interactionTypes", [])
                mech = interaction_types[0] if interaction_types else "N/A"
                rows.append({
                    "Drug": drug_name,
                    "ID": f"[{chembl_id}](https://www.ebi.ac.uk/chembl/compound_report_card/{chembl_id}/)" if chembl_id else "",
                    "Mechanism": mech,
                    "Approval": interaction.get("approvalStatus", "Unknown"),
                    "Source": "DGIdb",
                })

        if not rows and gene_symbol in FALLBACK_DRUGS:
            rows.extend(FALLBACK_DRUGS[gene_symbol])

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"[DGIdb] Error fetching for {gene_symbol}: {e}")
        if gene_symbol in FALLBACK_DRUGS:
            return pd.DataFrame(FALLBACK_DRUGS[gene_symbol])
        return pd.DataFrame()



# ---------- Open Targets ----------
def _ot_map_symbol_to_ensembl(gene_symbol: str) -> Optional[str]:
    """
    Use Open Targets mapIds to resolve a gene symbol to Ensembl ID.
    Returns e.g. 'ENSG00000141510' or None.
    """
    try:
        query = """
        query Map($terms: [String!]!) {
          mapIds(queryTerms: $terms, entityNames: ["target"]) {
            mappings {
              term
              hits { id name entity }
            }
          }
        }
        """
        payload = {"query": query, "variables": {"terms": [gene_symbol]}}
        r = requests.post(OT_GQL_URL, json=payload, headers=DEFAULT_HEADERS, timeout=30)
        r.raise_for_status()
        j = _safe_json(r)
        if not j or "data" not in j:
            return None
        mappings = (j["data"].get("mapIds", {}) or {}).get("mappings", []) or []
        for m in mappings:
            hits = m.get("hits", []) or []
            for h in hits:
                if h.get("entity") == "target" and h.get("id", "").startswith("ENSG"):
                    return h["id"]
        return None
    except Exception as e:
        print(f"OpenTargets mapIds error: {e}")
        return None


def fetch_from_opentargets(gene_symbol: str) -> pd.DataFrame:
    """
    Query Open Targets knownDrugs for a target (resolved from gene symbol).
    Returns columns: Drug, ID, Mechanism, Approval, Source
    """
    try:
        ensg = _ot_map_symbol_to_ensembl(gene_symbol)
        if not ensg:
            return pd.DataFrame()

        # knownDrugs query — no auth required
        query = """
        query KnownDrugs($ensemblId: String!) {
          target(ensemblId: $ensemblId) {
            approvedSymbol
            knownDrugs {
              count
              rows {
                drugId
                prefName
                mechanismOfAction
                phase
                diseaseId
                disease { name }
                approvedSymbol
              }
            }
          }
        }
        """
        variables = {"ensemblId": ensg}
        r = requests.post(OT_GQL_URL, json={"query": query, "variables": variables},
                          headers=DEFAULT_HEADERS, timeout=40)
        r.raise_for_status()
        j = _safe_json(r)
        if not j:
            return pd.DataFrame()
        if "errors" in j:
            print("OpenTargets GraphQL errors:", j["errors"])
            return pd.DataFrame()

        target = (j.get("data", {}) or {}).get("target", {}) or {}
        kd = target.get("knownDrugs", {}) or {}
        rows_gql = kd.get("rows", []) or []

        rows = []
        for row in rows_gql:
            phase = row.get("phase", None)
            phase_str = str(int(phase)) if isinstance(phase, (int, float)) else (
                str(phase) if phase is not None else "Unknown"
            )
            rows.append(
                {
                    "Drug": row.get("prefName", "") or "",
                    "ID": f"[{row.get('drugId','')}](https://www.ebi.ac.uk/chembl/compound_report_card/{row.get('drugId','')}/)" if row.get("drugId") else "",
                    "Mechanism": row.get("mechanismOfAction", "") or "",
                    "Approval": phase_str,
                    "Source": "OpenTargets",
                }
            )

        return pd.DataFrame(rows)

    except Exception as e:
        print(f"Error in OpenTargets fetch: {e}")
        return pd.DataFrame()


# ---------- Wrapper ----------
def fetch_drugs_for_gene(gene_symbol: str) -> pd.DataFrame:
    """
    Combine results from ChEMBL + OpenTargets + DGIdb + Fallback (DrugBank-curated).
    Always returns at least 1 row.
    """
    try:
        dfs = []

        # ChEMBL
        df_chembl = fetch_from_chembl(gene_symbol)
        if df_chembl is not None and not df_chembl.empty:
            dfs.append(df_chembl)

        # OpenTargets
        df_ot = fetch_from_opentargets(gene_symbol)
        if df_ot is not None and not df_ot.empty:
            dfs.append(df_ot)

        # DGIdb
        df_dgidb = fetch_from_dgidb(gene_symbol)
        if df_dgidb is not None and not df_dgidb.empty:
            dfs.append(df_dgidb)

        # Fallback (DrugBank-curated)
        if not dfs and gene_symbol.upper() in FALLBACK_DRUGS:
            dfs.append(pd.DataFrame(FALLBACK_DRUGS[gene_symbol.upper()]))

        # If still nothing
        if not dfs:
            return pd.DataFrame([{
                "Drug": "No drug data found",
                "ID": "",
                "Mechanism": "",
                "Approval": "",
                "Source": ""
            }])

        # Merge & clean
        df = pd.concat(dfs, ignore_index=True)
        for col in ["Drug", "ID", "Mechanism", "Approval", "Source"]:
            if col in df.columns:
                df[col] = df[col].fillna("")

        subset_cols = [c for c in ["ID", "Drug", "Mechanism", "Source"] if c in df.columns]
        df = df.drop_duplicates(subset=subset_cols, keep="first").reset_index(drop=True)

        final_cols = ["Drug", "ID", "Mechanism", "Approval", "Source"]
        return df[[c for c in final_cols if c in df.columns]]

    except Exception as e:
        print(f"Wrapper error: {e}")
        return pd.DataFrame([{
            "Drug": "Error fetching data",
            "ID": "",
            "Mechanism": "",
            "Approval": "",
            "Source": ""
        }])
