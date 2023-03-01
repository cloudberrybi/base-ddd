from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='cbi_ddd',
    zip_safe=True,
    version='1.0.2',
    description='Base CBI objects',
    url='https://github.com/cloudberrybi/base-ddd',
    maintainer='CloudberryBI',
    maintainer_email='cto@cloudberry.bi',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
