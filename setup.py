from setuptools import setup, find_packages

version = '1.0'

setup(
    name = "plone.recipe.zeoserver",
    version = version,
    author = "Hanno Schlichting",
    author_email = "hannosch@plone.org",
    description = "ZC Buildout recipe for installing a ZEO server",
    long_description = open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
    license = "ZPL 2.1",
    keywords = "zope2 zeo zodb buildout",
    url='http://pypi.python.org/pypi/plone.recipe.zeoserver',
    classifiers=[
        "License :: OSI Approved :: Zope Public License",
        "Framework :: Buildout",
        "Framework :: Zope2",
        "Programming Language :: Python",
    ],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['plone', 'plone.recipe'],
    install_requires = [
        'zc.buildout',
        'setuptools',
        'zc.recipe.egg',
        'ZODB3',
        'ZopeUndo',
    ],
    tests_require=['zope.testing'],
    zip_safe=False,
    entry_points = {
        'zc.buildout': ['default = plone.recipe.zeoserver:Recipe']
    },
    )
