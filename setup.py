import setuptools


def setup() -> None:
    with open('README.md') as readme_file:
        readme = readme_file.read()

    with open('LICENSE') as license_file:
        license = license_file.read()

    setuptools.setup(
        name='cypher-subgraph',
        version='0.1.0',
        description='A python library and CLI tool that rewrites and '
                    'generates cypher queries for supporting sub-graph.',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Alireza Roshanzamir',
        author_email='a.roshanzamir1996@gmail.com',
        url='https://github.com/AlirezaRoshanzamir/'
            'cypher-subgraph/tree/main/src/cypher_subgraph',
        license=license,
        include_package_data=True,
        install_requires=[
            'antlr4-python3-runtime==4.7.2',
            'click>=8.0.4,<9'
        ],
        entry_points={
            'console_scripts': [
                'cypher-subgraph = cypher_subgraph.cli:cypher_subgraph'
            ]
        },
        package_dir={'': 'src'},
        packages=setuptools.find_packages('src'),
        python_requires='>=3.7',
    )


if __name__ == '__main__':
    setup()
