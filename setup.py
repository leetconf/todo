from setuptools import setup, find_packages
from todo import __version__

setup(
    name='todo',
    version=__version__,
    description='a simple task manager cli',
    author='leet',
    packages=find_packages(include=['todo', 'todo.*']),
    include_package_data=True,
    package_data={
        'todo': ['data/*.json'],
    },
    entry_points={
        'console_scripts': [
            'todo=todo.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)