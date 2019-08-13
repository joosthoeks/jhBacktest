from setuptools import setup


setup(
    name='jhBacktest',
    version='20190813.0',
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
#        'statistics',
#        'numpy',
#        'tabulate',
#        'termcolor',
#        'matplotlib',
#        'jhtalib',
    ],
    dependency_links=[],
    zip_safe=False
)

