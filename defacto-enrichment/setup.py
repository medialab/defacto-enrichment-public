from setuptools import find_packages, setup

meta_package = {}
with open("./defacto_enrichment/__version__.py") as f:
    exec(f.read(), meta_package)

setup(
    name="defacto-enrichment",
    version=meta_package["__version__"],
    description="Script to manage transformation and enrichment of De Facto data.",
    author="Kelly Christensen",
    keywords="webmining",
    license="GPL-3.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=["schemas"]),
    install_requires=[
        "minall @ git+https://github.com/medialab/minall.git@v0.2.2",
        "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": ["defacto-enrichment=defacto_enrichment.main:main"],
    },
    zip_safe=True,
)
