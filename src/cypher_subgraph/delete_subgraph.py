def delete_subgraph(subgraph_id: str) -> str:
    return 'MATCH (v) OPTIONAL MATCH (v)-[e]-() ' \
           'REMOVE v.{} REMOVE e.{}'.format(subgraph_id, subgraph_id)
