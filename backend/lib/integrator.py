from typing import Dict, Any, List

def integrate_json(raw_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrates results from GestaltMatcher and PubCaseFinder into a unified format.
    ... (docstring continues)
    """
    print("--- Starting results integration ---")

    pcf_results_list = raw_results.get('pubcasefinder')

    if not pcf_results_list or not isinstance(pcf_results_list, list):
        print("No PubCaseFinder list found to integrate.")
        return raw_results

    # Step 1: Pre-process PubCaseFinder results
    pcf_by_omim = {}
    pcf_by_gene = {}

    for item in pcf_results_list:
        if item.get('id') and item['id'].startswith('OMIM:'):
            try:
                omim_id_str = item['id'].replace('OMIM:', '')
                pcf_by_omim[omim_id_str] = {'rank': item.get('rank'), 'score': item.get('score')}
            except (ValueError, TypeError):
                continue
        
        if item.get('hgnc_gene_symbol') and isinstance(item.get('hgnc_gene_symbol'), list):
            for gene_symbol in item['hgnc_gene_symbol']:
                pcf_by_gene[gene_symbol] = {'rank': item.get('rank'), 'score': item.get('score')}

    print(f"Created pcf_by_omim lookup with {len(pcf_by_omim)} entries.")
    if pcf_by_omim:
        print(f"  -> Sample OMIM keys from PCF: {list(pcf_by_omim.keys())[:5]}")

    print(f"Created pcf_by_gene lookup with {len(pcf_by_gene)} entries.")
    if pcf_by_gene:
        print(f"  -> Sample Gene keys from PCF: {list(pcf_by_gene.keys())[:5]}")
    
    # Step 2: Update 'syndromes' using the correct key
    syndrome_key = 'suggested_syndromes_list'
    if syndrome_key in raw_results:
        print(f"\n--- Checking '{syndrome_key}' for matches ---")
        match_count = 0
        for i, syndrome in enumerate(raw_results[syndrome_key]):
            omim_id = syndrome.get('omim_id')
            if i < 5:
                print(f"  - Attempting to match GM OMIM ID: '{str(omim_id)}'")
            if omim_id and str(omim_id) in pcf_by_omim:
                match_count += 1
                pcf_match = pcf_by_omim[str(omim_id)]
                syndrome['pubcasefinder_rank'] = pcf_match['rank']
                syndrome['pubcasefinder_score'] = pcf_match['score']
        print(f"Found {match_count} matches in '{syndrome_key}'.")

    # Step 3: Update 'genes' using the correct key
    gene_key = 'suggested_genes_list'
    if gene_key in raw_results:
        print(f"\n--- Checking '{gene_key}' for matches ---")
        match_count = 0
        for i, gene in enumerate(raw_results[gene_key]):
            gene_name = gene.get('gene_name')
            if i < 5:
                print(f"  - Attempting to match GM Gene Name: '{gene_name}'")
            if gene_name and gene_name in pcf_by_gene:
                match_count += 1
                pcf_match = pcf_by_gene[gene_name]
                gene['pubcasefinder_rank'] = pcf_match['rank']
                gene['pubcasefinder_score'] = pcf_match['score']
        print(f"Found {match_count} matches in '{gene_key}'.")

    # Step 4: Update 'patients' using the correct key
    patient_key = 'suggested_patients_list'
    if patient_key in raw_results:
        print(f"\n--- Checking '{patient_key}' for matches ---")
        match_count = 0
        for i, patient in enumerate(raw_results[patient_key]):
            omim_id = patient.get('omim_id')
            if i < 5:
                print(f"  - Attempting to match GM Patient OMIM ID: '{str(omim_id)}'")
            if omim_id and str(omim_id) in pcf_by_omim:
                match_count += 1
                pcf_match = pcf_by_omim[str(omim_id)]
                patient['pubcasefinder_rank'] = pcf_match['rank']
                patient['pubcasefinder_score'] = pcf_match['score']
        print(f"Found {match_count} matches in '{patient_key}'.")


    print("\n--- Integration complete ---")
    return raw_results
