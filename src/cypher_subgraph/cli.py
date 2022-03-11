import sys

import click

from cypher_subgraph.add_to_subgraph import add_to_subgraph
from cypher_subgraph.canonize_subgraph_id import canonize_subgraph_id
from cypher_subgraph.delete_subgraph import delete_subgraph
from cypher_subgraph.rewrite_for_subgraph import rewrite_for_subgraph


@click.group()
def cypher_subgraph() -> None:
    """Rewrite or generate query for supporting sub-graph feature."""
    pass


@cypher_subgraph.command(
    short_help='Rewrite the query read from standard input that the query '
    'returne values become the member of the specified "subgraph" argument.'
)
@click.argument('subgraph', type=str)
def add_to(subgraph: str) -> None:
    query = read_query_from_stdin()
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    adding_query = add_to_subgraph(query, canonical_subgraph_id)
    click.echo(adding_query)


@cypher_subgraph.command(
    short_help='Rewrite the query read from standard input that the query is '
    'executed only in the specified "subgraph" argument.'
)
@click.argument('subgraph', type=str)
def rewrite_for(subgraph: str) -> None:
    query = read_query_from_stdin()
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    rewritten_query = rewrite_for_subgraph(query, canonical_subgraph_id)
    click.echo(rewritten_query)


@cypher_subgraph.command(
    short_help='Generate a query for deleting specfied "subgraph" argument.'
)
@click.argument('subgraph', type=str)
def delete(subgraph: str) -> None:
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    delete_query = delete_subgraph(canonical_subgraph_id)
    click.echo(delete_query)


def read_query_from_stdin() -> str:
    return ''.join(line for line in sys.stdin)


if __name__ == '__main__':
    cypher_subgraph()
