from setuptools import setup, find_packages

setup(
    name='fastapi-rest',  
    version='0.1.0',
    description='A simple Python package called neel',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Indranil Swarnakar',
    author_email='indranil.swarnakar@gmail.com',
    url='https://github.com/neel/neel',  
    packages=find_packages(),  
    install_requires=[
        'fastapi', 'pydentic', 
        'sqlalchemy', 'uvicorn',
        'alembic'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'fastapi-rest = fastapi_rest.cli:main',  
        ],
    },
    include_package_data=True
)
