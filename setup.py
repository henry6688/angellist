from setuptools import setup

setup(
   name='website',
   version='1.0',
   description='Module to calculate fund allocation among investors',
   author='Henry',
   author_email='henry6688@gmail.com',
   packages=['website'],  # same as name
   install_requires=['ipywidgets'], # external packages as dependencies
)