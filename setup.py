from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Trading tools'

# Setting up
setup(
    name="xtrader",
    version=VERSION,
    author="Georgios Smyridis (georgesmyr)",
    author_email="<georgesmyr@icloud.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 2 - Development",
        "Intended Audience :: Retail Traders",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
