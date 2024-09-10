from setuptools import setup, find_packages

setup(
    name="rinex_download",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'rinex_downloader=rinex_downloader.cli:main',
        ],
    },
)