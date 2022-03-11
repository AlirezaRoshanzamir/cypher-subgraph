from inspect import cleandoc

import pytest

from cypher_subgraph import add_to_subgraph
from tests.utility import remove_whitespace

TEST_DATA = [
    [
        "MATCH (v) RETURN v",
        cleandoc(
            """
        MATCH (v) WITH v
        SET v.id = true
        """
        ),
    ],
    [
        "MATCH ()-[e]-() RETURN e",
        cleandoc(
            """
        MATCH ()-[e]-() WITH e
        SET e.id = true
        """
        ),
    ],
    [
        "MATCH p=()-[*2]-() RETURN p",
        cleandoc(
            """
        MATCH p=()-[*2]-() WITH p
        FOREACH (node in nodes(p) | SET node.id = true)
        FOREACH (relationship in relationships(p) | SET relationship.id = true)
        """
        ),
    ],
    [
        "MATCH (v1)-[e]-(v2) WHERE v1.name = v2.name RETURN v1, v2",
        cleandoc(
            """
        MATCH (v1)-[e]-(v2) WHERE v1.name = v2.name WITH v1, v2
        SET v1.id = true
        SET v2.id = true
        """
        ),
    ],
    [
        "MATCH p=(v1)-[e]-(v2) WHERE v1.name = v2.name RETURN p, v1, e",
        cleandoc(
            """
        MATCH p=(v1)-[e]-(v2) WHERE v1.name = v2.name WITH p, v1, e
        FOREACH (node in nodes(p) | SET node.id = true)
        FOREACH (relationship in relationships(p) | SET relationship.id = true)
        SET v1.id = true
        SET e.id = true
        """
        ),
    ],
]


@pytest.mark.parametrize("query, expected_adding_query", TEST_DATA)
def test_add_to_subgraph(query: str, expected_adding_query: str) -> None:
    # Arrange, Act
    actual_adding_query = add_to_subgraph(query, "id")

    # Assert
    assert remove_whitespace(actual_adding_query) == remove_whitespace(
        expected_adding_query
    )
