from setuptools import setup, find_packages

reqs = [
    "h5py",
    "jupyterlab",
    "matplotlib",
    "numpy",
    "pandas",
    "boto3",
    "yaml"
]

conda_reqs = [
    "h5py",
    "jupyterlab",
    "matplotlib",
    "numpy",
    "pandas",
    "boto3",
    "yaml"
]

test_pkgs = []

setup(
    name="terra-aws",
    python_requires='>3.4',
    description="AWS builds.",
    url="https://github.com/neumj/terra-aws",
    install_requires=reqs,
    conda_install_requires=conda_reqs,
    test_requires=test_pkgs,
    packages=find_packages(),
    include_package_data=True
)
