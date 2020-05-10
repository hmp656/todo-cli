from setuptools import setup
from setuptools import find_packages

setup(
    name='todo-cli',
    version='0.1',
    install_requires=['click',],
    packages=find_packages(),
    py_modules=['sqlite3', 'random', 
                'datetime', 'collections',
                'os', 'sys'],
    entry_points={
        'console_scripts': ['todo = todolist.todolist:main'],
    },
    python_requires=">=3.6"
)
