from setuptools import setup, find_packages
import os

version = '0.8'

setup(name='adi.commons',
      version=version,
      description="Some helpers-methods for often repeating and general purposes, to be used of other eggs.",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.md")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ida Ebkes',
      author_email='contact@ida-ebkes.eu',
      url='https://github.com/ida/adi.commons/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['adi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
