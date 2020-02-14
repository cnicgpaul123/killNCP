# -*- coding: utf-8 -*-
"""
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
from distutils.core import setup
from setuptools import find_packages


app_id = "drf_auth"
app_name = "django-restframework-auth"
app_description = "DjangoRestframework utils."
app_version = __import__(app_id).__version__
app_requires = [
]


setup(name=app_name,
      description=app_description,
      version=app_version,
      url="https://github.com/princeofdatamining/"+app_name,
      license="MIT License",
      packages=find_packages(exclude=["tests"]),
      install_requires=app_requires)
