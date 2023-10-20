from setuptools import find_packages, setup

setup(
    name="defacto-enrichment",
    version="0.0.1",
    description="Script to manage transformation and enrichment of De Facto data.",
    author="Kelly Christensen",
    keywords="webmining",
    license="GPL-3.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=["schemas"]),
    install_requires=["minall @ git+https://github.com/medialab/minall.git"],
    entry_points={
        "console_scripts": ["defacto-enrichment=src.main:main"],
    },
    zip_safe=True,
)
