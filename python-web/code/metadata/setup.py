from setuptools import setup

setup(
    name='metadata',
    py_modules=['metadata2'],
    entry_points={
        'paste.app_factory': ['main=metadata2:app_factory'],
        },
    )
