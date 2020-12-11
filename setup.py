from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
  name = 'ezbasti',         # How you named your package folder (MyLib)
  packages = ['ezbasti'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A python package that allows you to download MIST/MESA isochrones directly from their website',   # Give a short description about your library
  author = 'Dinil Bose P',                   # Type in your name
  author_email = 'dinilbose@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/dinilbose/ezbasti',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dinilbose/ezbasti',    # I explain this later on
  keywords = ['ezbasti'], # Keywords that define your package best
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 4 - Beta',# Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Science/Research',# Define that your audience are developers
    'Topic :: Scientific/Engineering :: Astronomy',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',# Again, pick a license
    'Programming Language :: Python :: 3',# Specify which pyhton versions that you want to support
  ], install_requires=['astropy'],setup_requires=["numpy"],
)

