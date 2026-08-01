# 📁 utils/drugs.py

import requests
import pandas as pd


# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

OPENTARGETS_API = (
    "https://api.platform.opentargets.org/api/v4/graphql"
)

CHEMBL_API = (
    "https://www.ebi.ac.uk/chembl/api/data"
)


HEADERS = {
    "User-Agent": "Gene2Trials/1.0"
}


# -------------------------------------------------------
# SAFE REQUESTS
# -------------------------------------------------------

def safe_post(query, variables=None):

    try:

        response = requests.post(
            OPENTARGETS_API,
            json={
                "query": query,
                "variables": variables or {}
            },
            headers=HEADERS,
            timeout=30
        )


        if response.status_code != 200:

            print(
                "OpenTargets Error:",
                response.text
            )

            return None


        data = response.json()


        if "errors" in data:

            print(
                "GraphQL Error:",
                data["errors"]
            )

            return None


        return data


    except Exception as e:

        print(
            "OpenTargets Exception:",
            e
        )

        return None




def safe_get(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )


        if response.status_code == 200:

            return response.json()


        return None


    except Exception as e:

        print(
            "Request Error:",
            e
        )

        return None



# -------------------------------------------------------
# STEP 1
# GENE SYMBOL → ENSEMBL ID
# -------------------------------------------------------

def get_ensembl_id_from_symbol(gene_symbol):


    query = """
    query searchTarget($symbol:String!){
      search(
        queryString:$symbol,
        entityNames:["target"],
        page:{
          index:0,
          size:1
        }
      ){
        hits{
          object{
            ... on Target{
              id
              approvedSymbol
            }
          }
        }
      }
    }
    """


    result = safe_post(
        query,
        {
            "symbol":gene_symbol
        }
    )


    try:

        return (
            result["data"]
            ["search"]
            ["hits"][0]
            ["object"]
            ["id"]
        )


    except:

        return None



# -------------------------------------------------------
# STEP 2
# OPENTARGETS DRUG CANDIDATES
# -------------------------------------------------------

def fetch_opentarget_drugs(gene_symbol):


    ensembl_id = get_ensembl_id_from_symbol(
        gene_symbol
    )


    if not ensembl_id:

        return pd.DataFrame()



    query = """
    query getDrugCandidates($id:String!){
      target(ensemblId:$id){
        drugAndClinicalCandidates{
          rows{
            id
            maxClinicalStage
            drug{
              id
              name
              maximumClinicalStage
            }
            diseases{
              disease{
                id
                name
              }
            }
          }
        }
      }
    }
    """



    result = safe_post(
        query,
        {
            "id":ensembl_id
        }
    )


    if not result:

        return pd.DataFrame()



    rows = (

        result["data"]
        ["target"]
        ["drugAndClinicalCandidates"]
        ["rows"]

    )



    output=[]



    for row in rows:


        drug = row.get(
            "drug"
        ) or {}



        disease_names=[]



        for d in row.get(
            "diseases",
            []
        ):


            disease = d.get(
                "disease"
            )


            if disease:

                disease_names.append(
                    disease.get(
                        "name",
                        ""
                    )
                )



        output.append({

            "Drug":
                drug.get(
                    "name",
                    ""
                ),


            "ChEMBL_ID":
                drug.get(
                    "id",
                    ""
                ),


            "Clinical Stage":
                row.get(
                    "maxClinicalStage",
                    ""
                ),


            "Disease":
                ", ".join(
                    disease_names
                ),

            "Source":
                "OpenTargets"


        })


    return pd.DataFrame(output)

# -------------------------------------------------------
# FINAL FUNCTION
# -------------------------------------------------------

def fetch_drugs_for_gene(gene):


    df = fetch_opentarget_drugs(
        gene
    )


    if df.empty:

        return pd.DataFrame([{

            "Drug":
                "No Drug Found",

            "ChEMBL_ID":
                "-",

            "Clinical Stage":
                "-",

            "Disease":
                "-",

            "Source":
                "-"

        }])


    df["Source"] = (
        "OpenTargets"
    )


    return df.reset_index(
        drop=True
    )
