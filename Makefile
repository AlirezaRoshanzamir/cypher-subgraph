PYTHON = pyauto

develop check_type test:
	tox -e $(PYTHON)-$@

lint fix_lint:
	tox -e $@

compile_cypher_grammar:
	antlr4 \
		-Dlanguage=Python3 \
		-no-listener \
		-visitor \
		-Xexact-output-dir \
		-o src/cypher_subgraph/generated/ \
		src/cypher_subgraph/Cypher.g4 \
	&& touch src/cypher_subgraph/generated/__init__.py

clean:
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .tox
