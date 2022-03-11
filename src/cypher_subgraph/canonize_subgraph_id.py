def canonize_subgraph_id(subgraph_id: str) -> str:
    SUBGRAPH_ID_PREFIX = '__subgraph_'
    if subgraph_id.startswith(SUBGRAPH_ID_PREFIX):
        return subgraph_id
    return SUBGRAPH_ID_PREFIX + subgraph_id
