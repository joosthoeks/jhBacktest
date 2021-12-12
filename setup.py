from setuptools import setup


setup(
    name='jhBacktest',
    version='20211212.0',
    description='Backtest and analysis trading strategy with Python',
    keywords='backtest analysis trading strategy',
    url='https://github.com/joosthoeks/jhBacktest',
    author='Joost Hoeks',
    author_email='joosthoeks@gmail.com',
    license='GNU',
    packages=[
        'jhbacktest',
        'jhbacktest.backtest',
    ],
    install_requires=[],
    dependency_links=[],
    zip_safe=False
)

