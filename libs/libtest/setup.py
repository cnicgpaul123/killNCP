from distutils.core import setup
from setuptools import find_packages


app_id = "libtest"
app_name = "python-libtest"
app_description = "Python utils."
app_version = __import__(app_id).__version__
app_requires = [
]


setup(name=app_name,
      description=app_description,
      version=app_version,
      url="https://github.com/princeofdatamining/"+app_name,
      packages=find_packages(exclude=["tests"]),
      install_requires=app_requires)