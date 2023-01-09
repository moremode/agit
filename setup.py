from setuptools import setup

setup(
    name="agit",
    version="0.0.1",
    description="git loader helper",
    packages=['agit'],
    install_requires=['click'],
    entry_points = {
        'console_scripts': ['agit=agit.agit:main'],
    }
) 
