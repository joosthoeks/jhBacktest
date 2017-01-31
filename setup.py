from setuptools import setup


setup(
    name='jhBacktestMini',
    version='20170124.0',
    description='Mini Backtest and analysis trading strategy with Python',
    keywords='backtest analysis trading strategy',
    url='https://github.com/joosthoeks/jhBacktestMini',
    author='Joost Hoeks',
    author_email='joosthoeks@gmail.com',
    license='GNU',
    packages=[
        'jhbacktestmini',
        'jhbacktestmini.data',
        'jhbacktestmini.graph',
        'jhbacktestmini.stats',
        'jhbacktestmini.strategy',
    ],
    install_requires=[
        'scipy',
        'numpy',
        'pandas',
        'ta-lib',
        'tabulate',
        'termcolor',
        'matplotlib',
        'yahoo-finance',
#        'ibpy',
    ],
    dependency_links=[
        'https://github.com/blampe/IbPy/tarball/master',
    ],
    zip_safe=False
)

