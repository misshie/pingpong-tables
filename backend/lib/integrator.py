from typing import Dict, Any, List

def _add_gm_rank_and_score(item_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes a raw list from GestaltMatcher to add gm_rank and score.
    """
    if not item_list:
        return []

    # 1. Add gm_rank based on the original list order (0-indexed -> 1-indexed)
    for i, item in enumerate(item_list):
        item['gm_rank'] = i + 1

    # 2. Calculate a normalized score based on the 'distance' property
    try:
        distances = [item['distance'] for item in item_list]
        min_dist = min(distances)
        max_dist = max(distances)
        dist_range = max_dist - min_dist

        if dist_range == 0:
            # Avoid division by zero if all distances are the same
            for item in item_list:
                item['score'] = 1.0
        else:
            for item in item_list:
                item['score'] = 1.0 - (item['distance'] - min_dist) / dist_range
    except (KeyError, ValueError):
        # If 'distance' is missing or the list is empty, assign a default score of None
        for item in item_list:
            item['score'] = None

    return item_list

def _add_meta_rank_to_list(item_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Helper function to calculate mean_rank, sort the list by it, and then add a final meta_rank.
    """
    if not item_list:
        return []

    # 1. Calculate mean_rank for each item where possible
    for item in item_list:
        gm_rank = item.get('gm_rank')
        pcf_rank = item.get('pubcasefinder_rank')
        if isinstance(gm_rank, (int, float)) and isinstance(pcf_rank, (int, float)):
            item['mean_rank'] = (gm_rank + pcf_rank) / 2
        else:
            item['mean_rank'] = None # Mark for sorting to the bottom

    # 2. Sort the list by mean_rank. Items with a valid mean_rank (not None) come first.
    item_list.sort(key=lambda x: (x.get('mean_rank') is None, x.get('mean_rank')))

    # 3. Add the final meta_rank based on the new sorted order
    for i, item in enumerate(item_list):
        item['meta_rank'] = i + 1
    
    return item_list

def integrate_json(raw_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrates results from GestaltMatcher and PubCaseFinder, calculates ranks
    and scores, and returns the unified format.
    """
    print("--- Starting results integration ---")

    # --- Step 1: Process raw GestaltMatcher lists to add gm_rank and score ---
    for key in ['suggested_syndromes_list', 'suggested_genes_list', 'suggested_patients_list']:
        if key in raw_results:
            raw_results[key] = _add_gm_rank_and_score(raw_results[key])

    pcf_results_list = raw_results.get('pubcasefinder')

    # --- Step 2: Enrich with PubCaseFinder data if available ---
    if pcf_results_list and isinstance(pcf_results_list, list):
        # Pre-process PubCaseFinder results for efficient lookups
        pcf_by_omim = {}
        pcf_by_gene = {}
        for item in pcf_results_list:
            if item.get('id') and item['id'].startswith('OMIM:'):
                omim_id_str = item['id'].replace('OMIM:', '')
                pcf_by_omim[omim_id_str] = {'pubcasefinder_rank': item.get('rank'), 'pubcasefinder_score': item.get('score')}
            if item.get('hgnc_gene_symbol') and isinstance(item.get('hgnc_gene_symbol'), list):
                for gene_symbol in item['hgnc_gene_symbol']:
                    pcf_by_gene[gene_symbol] = {'pubcasefinder_rank': item.get('rank'), 'pubcasefinder_score': item.get('score')}
        
        # Enrich syndromes and patients list
        for key in ['suggested_syndromes_list', 'suggested_patients_list']:
            if key in raw_results:
                for item in raw_results[key]:
                    omim_id = item.get('omim_id')
                    if omim_id and str(omim_id) in pcf_by_omim:
                        item.update(pcf_by_omim[str(omim_id)])
        
        # Enrich genes list
        if 'suggested_genes_list' in raw_results:
            for item in raw_results['suggested_genes_list']:
                gene_name = item.get('gene_name')
                if gene_name and gene_name in pcf_by_gene:
                    item.update(pcf_by_gene[gene_name])

    # --- Step 3: Apply meta-ranking to each list ---
    for key in ['suggested_syndromes_list', 'suggested_genes_list', 'suggested_patients_list']:
         if key in raw_results:
            raw_results[key] = _add_meta_rank_to_list(raw_results[key])

    print("--- Integration and meta-ranking complete ---")
    return raw_results
