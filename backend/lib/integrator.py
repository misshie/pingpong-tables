from typing import Dict, Any

def integrate_json(raw_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrates results from GestaltMatcher and PubCaseFinder into a unified format.

    This function enriches the GestaltMatcher results (syndromes, genes, patients)
    with ranking and scoring information from PubCaseFinder.

    Args:
        raw_results: A dictionary containing the raw outputs from different analyses.
                     Expected structure:
                     {
                         "genes": [...],
                         "syndromes": [...],
                         "patients": [...],
                         "pubcasefinder": { ... }  // This key is optional.
                     }

    Returns:
        The mutated raw_results dictionary with integrated information.
    """
    print("--- Starting results integration ---")

    pcf_data = raw_results.get('pubcasefinder')
    # Exit early if there's no PubCaseFinder data to integrate.
    if not pcf_data or 'results' not in pcf_data:
        print("No PubCaseFinder data found to integrate.")
        return raw_results

    # --- Step 1: Pre-process PubCaseFinder results for efficient lookups ---
    
    pcf_by_omim = {}
    pcf_by_gene = {}

    for item in pcf_data.get('results', []):
        # Create a lookup map for OMIM IDs
        if item.get('id') and item['id'].startswith('OMIM:'):
            try:
                omim_id_str = item['id'].replace('OMIM:', '')
                pcf_by_omim[omim_id_str] = {
                    'rank': item.get('rank'),
                    'score': item.get('score')
                }
            except (ValueError, TypeError):
                # Skip if OMIM ID format is invalid
                continue
        
        # Create a lookup map for gene symbols
        if item.get('hgnc_gene_symbol'):
            gene_symbol = item['hgnc_gene_symbol']
            pcf_by_gene[gene_symbol] = {
                'rank': item.get('rank'),
                'score': item.get('score')
            }

    # --- Step 2: Update 'syndromes' with PubCaseFinder data ---
    
    if 'syndromes' in raw_results:
        print("Integrating with 'syndromes'...")
        for syndrome in raw_results['syndromes']:
            omim_id = syndrome.get('omim_id')
            if omim_id and str(omim_id) in pcf_by_omim:
                pcf_match = pcf_by_omim[str(omim_id)]
                syndrome['pubcasefinder_rank'] = pcf_match['rank']
                syndrome['pubcasefinder_score'] = pcf_match['score']

    # --- Step 3: Update 'genes' with PubCaseFinder data ---

    if 'genes' in raw_results:
        print("Integrating with 'genes'...")
        for gene in raw_results['genes']:
            gene_name = gene.get('gene_name') # As per your instruction
            if gene_name and gene_name in pcf_by_gene:
                pcf_match = pcf_by_gene[gene_name]
                gene['pubcasefinder_rank'] = pcf_match['rank']
                gene['pubcasefinder_score'] = pcf_match['score']

    # --- Step 4: Update 'patients' with PubCaseFinder data ---

    if 'patients' in raw_results:
        print("Integrating with 'patients'...")
        for patient in raw_results['patients']:
            omim_id = patient.get('omim_id')
            if omim_id and str(omim_id) in pcf_by_omim:
                pcf_match = pcf_by_omim[str(omim_id)]
                patient['pubcasefinder_rank'] = pcf_match['rank']
                patient['pubcasefinder_score'] = pcf_match['score']

    print("--- Integration complete ---")

    return raw_results
