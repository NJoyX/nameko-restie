from setuptools import setup, find_packages

setup(
    name='nameko-restie',
    version='0.1',
    description='@TODO',
    long_description='@TODO',
    author='Fill Q',
    author_email='fill@njoyx.net',
    url='https://github.com/NJoyX/nameko-restie',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=[
        "nameko",
        "marshmallow",
        "pytz",
        "six",
        "apispec",
        "validators",
        # "msgpack-python"
    ],
    entry_points={
        'console_scripts': [
            'restiectl=restie.cli.main:main',
        ],
    },
    include_package_data=True,
    zip_safe=True,
    keywords=['nameko', 'restie', 'rest', 'werkzeug'],
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
