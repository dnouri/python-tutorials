from setuptools import setup

setup(
    name='commenter',
    py_modules=['commenter12'],
    entry_points={
        'paste.filter_factory': ['main=commenter12:commenter_filter_factory'],
        },
    )
