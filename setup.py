from setuptools import setup, find_packages


setup(
    name='modelkfsapi',
    author='Len Strnad',
    version='0.1',
    install_requires=[
        'pandas',
        'numpy',
        'torch',
        'lmdb',
        'scikit-learn',
        'pytest'
    ],
    packages=find_packages(),
    license='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_ok=False

)
