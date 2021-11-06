import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#     reqs = fh.readlines()

setuptools.setup(
    name="biblearn",
    version="0.0.2",
    author="Seth S. Henshaw",
    author_email="seth.henshaw@gmail.com",
    description="Biblical Learning Toolkit (biblearn)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hensh2ss/biblearn",
    project_urls={
        "Bug Tracker": "https://github.com/hensh2ss/biblearn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    package_data={'biblearn':['resources/sword/*.zip',"requirements.txt"]},
    install_requires=['pysword']
)