from setuptools import setup

setup(
    name="echochamber",
    version="0.0.1",
    url="https://github.com/equalitie/EchoChamber",
    packages=["echochamber"],
    package_data={"echochamber": ["templates/*"]},
    zip_safe=False,
    install_requires=[
        "Jinja2",
        "pyyaml",
        "pexpect",
    ],
)
