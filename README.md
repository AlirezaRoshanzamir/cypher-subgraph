# cypher-subgraph
A python library and CLI tool that rewrites and generates cypher queries for supporting subgraph.

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
               returned values become the member of the specified "subgraph"
               argument.
  delete       Generate a query for deleting specfied "subgraph" argument.
  rewrite-for  Rewrite the query read from standard input that the query is
               executed only in the specified "subgraph" argument.
````

# Examples
There is no known limitation on the reading queries. All the commands work well
with Cypher **nodes**, **edges**, and **paths**.

Currently, running commands on multiple subgraphs at the same time is not
supported. You should pass the previous rewritten query again to rewrite
queries for multiple subgraphs.

## add-to

Rewriting the query which the returned values becomes the member of "sg"
subgraph:
```
cypher-subgraph add-to sg << EOF
MATCH (v) RETURN v
EOF
```

returns:
```
MATCH (v) WITH v
SET v.__subgraph_sg = true
```

## rewrite-for

Rewrite the query which it only will be executed in the "sg" subgraph:

```
cypher-subgraph rewrite-for sg << EOF
MATCH (v) RETURN v
EOF
```

returns:
```
MATCH (v { __subgraph_sg: true }) RETURN v
```

## delete
Delete subgraph "sg" meta-data:
```
cypher-subgraph delete sg
```

returns:
```
MATCH (v) OPTIONAL MATCH (v)-[e]-() REMOVE v.__subgraph_sg REMOVE e.__subgraph_sg
```

# Implementation

The tool mimics the subgraph feature using the addition property for the nodes
and edges. For each node and edge which is inside the "x" subgraph, the
property "__subgraph_x" will be set true.
