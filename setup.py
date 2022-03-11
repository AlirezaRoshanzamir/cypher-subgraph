import setuptools


def setup() -> None:
    with open('README.md') as readme_file:
        readme = readme_file.read()

    with open('LICENSE') as license_file:
        license = license_file.read()

    setuptools.setup(
        name='cypher-subgraph',
        version='0.1.0',
        description='...',
        long_description=readme,
        author='Alireza Roshanzamir',
        author_email='a.roshanzamir1996@gmail.com',
        url='...',
        license=license,
        include_package_data=True,
        install_requires=[
            'antlr4-python3-runtime==4.7.2',
            'click>=8.0.4,<9'
        ],
        entry_points={
            'console_scripts': ['cypher-subgraph = cypher_subgraph.cli:cli']
        },
        package_dir={'': 'src'},
        packages=setuptools.find_packages('src'),
        python_requires='>=3.7',
    )


if __name__ == '__main__':
    setup()
