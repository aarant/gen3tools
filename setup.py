from setuptools import setup

from __init__ import __version__, url

with open('README.md', 'r') as f:
    long_description = f.read()


setup(name='poketools',
      version=__version__,
      description='Tools for TASing and data analysis of Gen 3 Pokemon games',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ariel A',
      author_email='arantonitis@gmail.com',
      url=url,
      packages=['poketools'],
      package_dir={'poketools': ''},
      package_data={'*': []},
      include_package_data=True,
      entry_points={'gui_scripts': ['poketools = poketools.gui:main']},
      license='LICENSE',
      # See https://pypi.org/classifiers/
      classifiers=[],
      install_requires=['PyQt5>=5.13'],
      python_requires='>=3.6')
