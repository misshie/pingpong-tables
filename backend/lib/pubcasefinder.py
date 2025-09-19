import requests
import json
from typing import List, Dict, Any

# The actual PubCaseFinder API endpoint URL
PUBCASEFINDER_API_URL = "https://pubcasefinder.dbcls.jp/api/pcf_get_ranked_list"

def query_pubcasefinder(hpo_ids: List[str]) -> Dict[str, Any]:
    """
    Queries the PubCaseFinder API with a list of HPO IDs.

    Args:
        hpo_ids: A list of HPO term IDs (e.g., ["HP:0000175", "HP:0000750"]).

    Returns:
        A dictionary containing the API response, or an error message if the query fails.
    """
    if not hpo_ids:
        # Return an empty dictionary if no HPO IDs are provided.
        return {}

    print(f"Querying PubCaseFinder with HPO IDs: {hpo_ids}")

    # Construct the parameters for the GET request.
    params = {
        'target': 'omim',
        'format': 'json',
        'hpo_id': ','.join(hpo_ids)  # Join the list into a comma-separated string.
    }

    try:
        # Make the GET request to the PubCaseFinder API with a 30-second timeout.
        response = requests.get(PUBCASEFINDER_API_URL, params=params, timeout=30)
        
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code.
        response.raise_for_status()
        

       # --- Debugging Output Start ---
        print("--- PubCaseFinder API Response ---")
        # Pretty-print the JSON response to the console for debugging.
    
        print(json.dumps(response.json() , indent=2)[:500] + "\n...")

        print("---------------------------------")
        # --- Debugging Output End ---



        # Parse the JSON response and return it.
        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error querying PubCaseFinder: {e}")
        return {"error": "Failed to connect to the PubCaseFinder API."}

