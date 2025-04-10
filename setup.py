from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "3.0.5.dev0"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.recipe.zeoserver",
    version=version,
    author="Hanno Schlichting",
    author_email="hannosch@plone.org",
    description="ZC Buildout recipe for installing a ZEO server",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="ZPL 2.1",
    keywords="zope2 zeo zodb buildout",
    url="https://github.com/plone/plone.recipe.zeoserver",
    download_url="https://pypi.org/project/plone.recipe.zeoserver",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Zope Public License",
        "Framework :: Buildout",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.8",
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    namespace_packages=["plone", "plone.recipe"],
    install_requires=[
        "setuptools",
        "zc.buildout",
        "zc.recipe.egg",
        "zdaemon",
        "ZEO",
        "ZODB >= 5",
        "zope.mkzeoinstance >= 5.1.1",
        "ZopeUndo",
    ],
    extras_require={"zrs": ["zc.zrs"]},
    zip_safe=False,
    entry_points={
        "zc.buildout": ["default = plone.recipe.zeoserver.recipe:Recipe"],
    },
)
