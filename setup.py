import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physwiki", 
    version="0.0.11",
    author="Richard Peschke",
    author_email="peschke@hawaii.edu",
    description="",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "pandoc",
       "pylatexenc",
       "watchdog"
    ],
    python_requires='>=3.8',
    
    entry_points = {
        'console_scripts': ['physwiki=physwiki.bin_physwiki:main',
                            'physwiki_updateMD=physwiki.bin_markdown_refs:main'
                            ],
    }
)
