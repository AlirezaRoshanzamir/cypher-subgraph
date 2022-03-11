PYTHON = pyauto

develop check_types test:
	tox -e $(PYTHON)-$@

lint fix_lint distribute:
	tox -e $@

compile_cypher_grammar: ensure_antlr4
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

ensure_antlr4:
	sudo apt-get install antlr4=4.7.2*
