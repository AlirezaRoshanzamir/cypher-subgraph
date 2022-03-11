from typing import Any

from antlr4 import ParserRuleContext, TerminalNode  # type: ignore

from cypher_subgraph.generated.CypherParser import CypherParser
from cypher_subgraph.generated.CypherVisitor import CypherVisitor
from cypher_subgraph.parse_cypher import parse_cypher
from cypher_subgraph.visitor_common_functions_mixin import \
    VisitorCommonFunctionsMixin


def rewrite_for_subgraph(query: str, subgraph_id: str) -> str:
    tree = parse_cypher(query)
    visitor = QueryRewriterForSubgraph(subgraph_id)
    visitor.visit(tree)
    return visitor.rewritten_query


class QueryRewriterForSubgraph(CypherVisitor, VisitorCommonFunctionsMixin):
    def __init__(self, subgraph_id: str) -> None:
        super().__init__()
        self._subgraph_id = subgraph_id
        self._is_in_properties = False
        self._rewritten_query = ''

    @property
    def rewritten_query(self) -> str:
        return self._rewritten_query

    def visitOC_NodePattern(
        self, ctx: CypherParser.OC_NodePatternContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if i == ctx.getChildCount() - 1 and ctx.oC_Properties() is None:
                self._rewritten_query += \
                    ' {{ {}: true }}'.format(self._subgraph_id)

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_Properties(
        self, ctx: CypherParser.OC_PropertiesContext
    ) -> Any:
        self._is_in_properties = True
        result = self.visitChildren(ctx)
        self._is_in_properties = False
        return result

    def visitOC_MapLiteral(
        self, ctx: CypherParser.OC_MapLiteralContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if i == ctx.getChildCount() - 1 and self._is_in_properties:
                self._rewritten_query += \
                    ', {}: true '.format(self._subgraph_id)

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_RelationshipPattern(
        self, ctx: CypherParser.OC_RelationshipPatternContext
    ) -> Any:
        previous_visited_child_text = ''

        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            nonlocal previous_visited_child_text
            if ctx.oC_RelationshipDetail() is None \
                    and previous_visited_child_text == '-' \
                    and child_ctx.getText() == '-':
                self._rewritten_query += \
                    '[{{ {}: true }}]'.format(self._subgraph_id)
            previous_visited_child_text = child_ctx.getText()

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_RelationshipDetail(
        self, ctx: CypherParser.OC_RelationshipDetailContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if i == ctx.getChildCount() - 1 and ctx.oC_Properties() is None:
                self._rewritten_query += \
                    '{{ {}: true }}'.format(self._subgraph_id)

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitTerminal(self, node: TerminalNode) -> None:
        if str(node) != '<EOF>':
            self._rewritten_query += str(node)
        return super().visitTerminal(node)
