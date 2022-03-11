from typing import Any, Callable, Optional

from antlr4 import ParserRuleContext, ParseTreeVisitor  # type: ignore


class VisitorCommonFunctionsMixin(ParseTreeVisitor):
    def enhanced_visit_children(
        self,
        ctx: ParserRuleContext,
        before_hook: Optional[Callable[[int, ParserRuleContext], None]] = None,
        after_hook: Optional[Callable[[int, ParserRuleContext], None]] = None,
    ) -> Any:
        result = self.defaultResult()
        n = ctx.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(ctx, result):
                return result

            c = ctx.getChild(i)

            if before_hook is not None:
                before_hook(i, c)

            childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)

            if after_hook is not None:
                after_hook(i, c)

        return result
