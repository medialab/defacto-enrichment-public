from setuptools import find_packages, setup

setup(
    name="defacto-enrichment",
    version="0.0.2",
    description="Script to manage transformation and enrichment of De Facto data.",
    author="Kelly Christensen",
    keywords="webmining",
    license="GPL-3.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=["schemas"]),
    install_requires=[
        "minall @ git+https://github.com/medialab/minall.git@v0.0.9",
        "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": ["defacto-enrichment=defacto_enrichment.main:main"],
    },
    zip_safe=True,
)
