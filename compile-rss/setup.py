from setuptools import find_packages, setup

setup(
    name="compile-rss",
    version="0.0.1",
    description="Script to manage transformation and enrichment of De Facto data.",
    author="Kelly Christensen",
    keywords="webmining",
    license="GPL-3.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=["schemas"]),
    install_requires=[
        "minall @ git+https://github.com/medialab/minall.git@v0.0.6",
        "defacto-enrichment @ git+https://github.com/medialab/defacto-enrichment-public.git#subdirectory=defacto-enrichment",
        "requests==2.31.0",
        "GitPython==3.1.40",
        "click==8.1.7",
    ],
    entry_points={
        "console_scripts": ["compile-rss=src.cli:cli"],
    },
    zip_safe=True,
)
