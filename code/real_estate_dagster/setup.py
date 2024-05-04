from setuptools import find_packages, setup

setup(
    name="real_estate_dagster",
    packages=find_packages(exclude=["real_estate_dagster_tests"]),
    install_requires=[
        "dagster"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
