from antlr4 import (CommonTokenStream, InputStream,  # type: ignore
                    ParserRuleContext)

from cypher_subgraph.generated.CypherLexer import CypherLexer
from cypher_subgraph.generated.CypherParser import CypherParser


def parse_cypher(query: str) -> ParserRuleContext:
    input_stream = InputStream(query)
    lexer = CypherLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CypherParser(token_stream)
    return parser.oC_Cypher()
