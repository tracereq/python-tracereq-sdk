from setuptools import find_packages, setup

setup(
    name='tracereq',
    setup_requires=['wheel'],
    packages=['tracereq'],
    include_package_data=True,
    version='1.0.0',
    author='Prateek Sachan',
    author_email="ps@prateeksachan.com",
    license='MIT',
    python_requires=">=3.6",
    install_requires=['urllib3>=1.26.11; python_version >="3.6"']
)
