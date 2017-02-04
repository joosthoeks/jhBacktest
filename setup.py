from setuptools import setup


setup(
    name='jhBacktest',
    version='20170204.0',
    description='Backtest and analysis trading strategy with Python',
    keywords='backtest analysis trading strategy',
    url='https://github.com/joosthoeks/jhBacktest',
    author='Joost Hoeks',
    author_email='joosthoeks@gmail.com',
    license='GNU',
    packages=[
        'jhbacktest',
        'jhbacktest.data',
        'jhbacktest.graph',
        'jhbacktest.stats',
        'jhbacktest.strategy',
    ],
    install_requires=[
#        'scipy',
#        'numpy',
#        'pandas',
#        'ta-lib',
#        'tabulate',
#        'termcolor',
#        'matplotlib',
    ],
    dependency_links=[],
    zip_safe=False
)

