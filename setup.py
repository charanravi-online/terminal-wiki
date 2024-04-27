from setuptools import setup

setup(
    name='wiki',
    version='1.0',
    description='A simple CLI tool to fetch Wikipedia summaries.',
    py_modules=['wiki'],
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'wiki=wiki:main',
        ],
    },
)
