from cypher_subgraph import delete_subgraph


def test_delete_subgraph() -> None:
    # Arrange
    subgraph_id = "id"

    # Act
    query = delete_subgraph(subgraph_id)

    # Assert
    assert query == \
        "MATCH (v) OPTIONAL MATCH (v)-[e]-() REMOVE v.id REMOVE e.id"
