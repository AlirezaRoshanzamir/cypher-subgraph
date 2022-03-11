from typing import Any, Dict, Set

from antlr4 import ParserRuleContext, TerminalNode  # type: ignore

from cypher_subgraph.generated.CypherParser import CypherParser
from cypher_subgraph.generated.CypherVisitor import CypherVisitor
from cypher_subgraph.parse_cypher import parse_cypher
from cypher_subgraph.visitor_common_functions_mixin import \
    VisitorCommonFunctionsMixin


def add_to_subgraph(query: str, subgraph_id: str) -> str:
    tree = parse_cypher(query)
    visitor = QueryResultsTwoSubgraphAdder(subgraph_id)
    visitor.visit(tree)
    return visitor.generated_including_subgraph_query


class QueryResultsTwoSubgraphAdder(CypherVisitor, VisitorCommonFunctionsMixin):
    def __init__(self, subgraph_id: str) -> None:
        self._subgraph_id = subgraph_id
        self._generated_including_subgraph_query = ''
        self._type = ''
        self._each_variable_type: Dict[str, str] = {}
        self._returned_variables: Set[str] = set()
        self._is_variable = False
        self._is_node_or_relation_variable = False
        self._is_path_variable = False
        self._is_in_return = False

    @property
    def generated_including_subgraph_query(self) -> str:
        return self._generated_including_subgraph_query

    def visitOC_Variable(
        self, ctx: CypherParser.OC_VariableContext
    ) -> Any:
        self._is_variable = True
        result = super().visitOC_Variable(ctx)
        self._is_variable = False
        return result

    def visitOC_PatternPart(
        self, ctx: CypherParser.OC_PatternPartContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if isinstance(child_ctx, CypherParser.OC_VariableContext):
                self._each_variable_type[child_ctx.getText()] = 'path'

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_NodePattern(
        self, ctx: CypherParser.OC_NodePatternContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if isinstance(child_ctx, CypherParser.OC_VariableContext):
                self._each_variable_type[child_ctx.getText()] = 'node'

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_RelationshipDetail(
        self, ctx: CypherParser.OC_RelationshipDetailContext
    ) -> Any:
        def before_visiting_child_hook(
            i: int, child_ctx: ParserRuleContext
        ) -> None:
            if isinstance(child_ctx, CypherParser.OC_VariableContext):
                self._each_variable_type[child_ctx.getText()] = 'relationship'

        return self.enhanced_visit_children(
            ctx, before_hook=before_visiting_child_hook)

    def visitOC_Return(self, ctx: CypherParser.OC_ReturnContext) -> Any:
        self._is_in_return = True
        result = super().visitOC_Return(ctx)
        self._is_in_return = False
        return result

    def visitOC_ProjectionItem(
        self, ctx: CypherParser.OC_ProjectionItemContext
    ) -> Any:
        if ctx.getText() in self._each_variable_type:
            self._returned_variables.add(ctx.getText())
        return super().visitOC_ProjectionItem(ctx)

    def visitTerminal(self, node: TerminalNode) -> Any:
        if str(node).upper() == 'RETURN':
            self._generated_including_subgraph_query += 'WITH'
        elif str(node) == '<EOF>':
            self._add_set_clauses_to_generated_including_subgraph_query()
        else:
            self._generated_including_subgraph_query += str(node)
        return super().visitTerminal(node)

    def _add_set_clauses_to_generated_including_subgraph_query(self) -> None:
        for variable_name, variable_type in self._each_variable_type.items():
            if variable_name not in self._returned_variables:
                continue

            if variable_type in ('node', 'relationship'):
                self._generated_including_subgraph_query += \
                    '\nSET {}.{} = true'.format(
                        variable_name, self._subgraph_id)
            elif variable_type == 'path':
                self._generated_including_subgraph_query += \
                    '\nFOREACH (node in nodes({}) ' \
                    '| SET node.{} = true)'.format(
                        variable_name, self._subgraph_id)
                self._generated_including_subgraph_query += \
                    '\nFOREACH (relationship in relationships({}) ' \
                    '| SET relationship.{} = true)'.format(
                        variable_name, self._subgraph_id)
