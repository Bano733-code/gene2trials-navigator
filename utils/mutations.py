# 📁 utils/mutations.py
import requests

def fetch_mutations(gene_symbol):
    try:
        url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=dbsnp,cadd,snpeff,hgvs"
        res = requests.get(url)
        res.raise_for_status()
        hits = res.json().get("hits", [])

        mutations = []
        for hit in hits:
            # --- dbSNP rsID ---
            dbsnp_data = hit.get("dbsnp", {})
            rsid = dbsnp_data.get("rsid", "N/A")
            if isinstance(rsid, list):
                rsid = ", ".join(rsid)
            elif not rsid:
                rsid = "N/A"

            # --- CADD score ---
            cadd_data = hit.get("cadd", {})
            cadd_score = cadd_data.get("phred", "N/A")
            try:
                cadd_score = float(cadd_score)
            except:
                cadd_score = "N/A"

            # --- Mutation name (protein-level) ---
            mutation_name = "N/A"

            # 1. Check snpEff
            snpeff_data = hit.get("snpeff", {})
            if isinstance(snpeff_data, dict):
                ann = snpeff_data.get("ann", [])
                if isinstance(ann, list) and ann:
                    for entry in ann:
                        if isinstance(entry, dict) and "hgvs_p" in entry:
                            mutation_name = entry["hgvs_p"]
                            break

            # 2. Fallback: HGVS strings
            if mutation_name == "N/A":
                hgvs_data = hit.get("hgvs", [])
                if isinstance(hgvs_data, list):
                    for item in hgvs_data:
                        if isinstance(item, str) and "p." in item:
                            mutation_name = item.split(":")[-1]
                            break
                elif isinstance(hgvs_data, str) and "p." in hgvs_data:
                    mutation_name = hgvs_data.split(":")[-1]

            # --- Risk level classification ---
            risk_level = "N/A"
            if isinstance(cadd_score, (int, float)):
                if cadd_score >= 20:
                    risk_level = "🔴 High"
                elif cadd_score >= 10:
                    risk_level = "🟡 Moderate"
                else:
                    risk_level = "🟢 Low"

            # ✅ Make variant_id clickable (to MyVariant.info)
            variant_id = hit.get("_id", "N/A")
            if variant_id != "N/A":
                variant_id = f'<a href="https://myvariant.info/v1/variant/{variant_id}" target="_blank">{variant_id}</a>'
           
            variant = {
                "variant_id": variant_id,
                "mutation_name": mutation_name,
                "dbsnp": rsid,
                "cadd_score": cadd_score,
                "risk_level": risk_level
            }
            mutations.append(variant)

        return mutations
    except Exception as e:
        return f"Error fetching mutations: {e}"
