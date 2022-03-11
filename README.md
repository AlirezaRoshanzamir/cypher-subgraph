# cypher-subgraph
A python library and CLI tool that rewrites and generates cypher queries for supporting sub-graph.

# Installation
````
pip install cypher-subgraph
````

# CLI
````
Usage: cypher-subgraph [OPTIONS] COMMAND [ARGS]...

  Rewrite or generate query for supporting sub-graph feature.

Options:
  --help  Show this message and exit.

Commands:
  add-to       Rewrite the query read from standard input that the query
               returne values become the member of the specified "subgraph"
               argument.
  delete       Generate a query for deleting specfied "subgraph" argument.
  rewrite-for  Rewrite the query read from standard input that the query is
               executed only in the specified "subgraph" argument.
````
