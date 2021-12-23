from setuptools import find_packages, setup

INSTALL_REQUIRES = ["django==2.2"]

setup(
    name="django-test",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.9",
    url="https://github.com/LaurenceWarne/django-test",
    version="0.1",
    author="Laurence Warne",
    license="MIT",
    install_requires=INSTALL_REQUIRES
)
