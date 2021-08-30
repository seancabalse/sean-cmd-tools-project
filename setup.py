import setuptools

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="seancabalse_bulk_renamer_project",
    version="0.0.1",
    author="Sean Cabalse",
    author_email="seancabalse.dev@gmail.com",
    description="Package that rename all files that match a filter pattern in the target directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://vcs.bigcorp.xyz/devops/cmd_tools_project",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=(
    'requests',
    ),
)