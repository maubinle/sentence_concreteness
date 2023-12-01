import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentence_concreteness",
    version="0.0.0",
    author="Marianne Aubin Le Quere",
    author_email="msa258@cornell.edu",
    description="A function to tag sentences with a validated measure of sentence concreteness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maubinle/sentence_concreteness.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)