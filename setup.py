from setuptools import setup, find_packages

setup(
    name='banxicoapi',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyyaml'
    ],
    author='Elias Manjarrez',
    author_email='miguel.elias.g.manjarrez@gnail.com',
    description='Client for Banxico API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EliasManj/banxico-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
