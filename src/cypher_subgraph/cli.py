import sys

import click

from cypher_subgraph.add_to_subgraph import add_to_subgraph
from cypher_subgraph.canonize_subgraph_id import canonize_subgraph_id
from cypher_subgraph.delete_subgraph import delete_subgraph
from cypher_subgraph.rewrite_for_subgraph import rewrite_for_subgraph


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('subgraph', type=str)
def add_to(subgraph: str) -> None:
    query = read_query_from_stdin()
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    adding_query = add_to_subgraph(query, canonical_subgraph_id)
    click.echo(adding_query)


@cli.command()
@click.argument('subgraph', type=str)
def rewrite_for(subgraph: str) -> None:
    query = read_query_from_stdin()
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    rewritten_query = rewrite_for_subgraph(query, canonical_subgraph_id)
    click.echo(rewritten_query)


@cli.command()
@click.argument('subgraph', type=str)
def delete(subgraph: str) -> None:
    canonical_subgraph_id = canonize_subgraph_id(subgraph)
    delete_query = delete_subgraph(canonical_subgraph_id)
    click.echo(delete_query)


def read_query_from_stdin() -> str:
    return ''.join(line for line in sys.stdin)


if __name__ == '__main__':
    cli()
