import pytest

from cypher_subgraph import rewrite_for_subgraph
from tests.utility import remove_whitespace

TEST_DATA = [
    ["MATCH (v) RETURN v", "MATCH (v { id: true }) RETURN v"],
    ["MATCH (v:L) RETURN v", "MATCH (v: L { id: true }) RETURN v"],
    [
        'MATCH (v { property: "value" }) RETURN v',
        'MATCH (v { property: "value", id: true }) RETURN v',
    ],
    [
        "MATCH ()-[e]-() RETURN e",
        "MATCH ({ id: true })-[e { id: true }]-({ id: true }) RETURN e",
    ],
    [
        "MATCH p=()--() RETURN p",
        "MATCH p=({ id: true })-[{ id: true }]-({ id: true}) RETURN p",
    ],
    [
        "MATCH p=()-->() RETURN p",
        "MATCH p=({ id: true })-[{ id: true }]->({ id: true}) RETURN p",
    ],
    [
        "MATCH p=()<--() RETURN p",
        "MATCH p=({ id: true })<-[{ id: true }]-({ id: true}) RETURN p",
    ],
]


@pytest.mark.parametrize("query, expected_rewritten_query", TEST_DATA)
def test_rewrite_for_subgraph(
    query: str, expected_rewritten_query: str
) -> None:
    # Arrange, Act
    actual_rewritten_query = rewrite_for_subgraph(query, "id")

    # Assert
    assert remove_whitespace(actual_rewritten_query) == remove_whitespace(
        expected_rewritten_query
    )
