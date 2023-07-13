import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whistleaio",
    version="0.1.2",
    author="Robert Drinovac",
    author_email="unlisted@gmail.com",
    description="Asynchronous Python library for Whistle's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RobertD502/whistleaio',
    keywords='whistle, whistle fit, whistle api, whistle client, whistle gps, whistle pet',
    packages=setuptools.find_packages(),
    python_requires= ">=3.7",
    install_requires=[
        "aiohttp>=3.8.1",
        "strenum>=0.4.8",
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
    project_urls={  # Optional
    'Bug Reports': 'https://github.com/RobertD502/whistleaio/issues',
    'Source': 'https://github.com/RobertD502/whistleaio/',
    },
)
