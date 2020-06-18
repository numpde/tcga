import setuptools

# with open("README.md", 'r') as fd:
#     long_description = fd.read()

setuptools.setup(
    name="tcga",
    version="0.0.7",
    author="RA",
    author_email="numpde@null.net",
    keywords="computational biology bioinformatics genetics",
    description="Computational biology & bioinformatics utils",
    long_description="Please see the [github page](https://github.com/numpde/tcga).",
    long_description_content_type="text/markdown",
    url="https://github.com/numpde/tcga",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[''],

    test_suite="nose.collector",
    tests_require=["nose"],
)
