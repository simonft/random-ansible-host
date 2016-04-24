from setuptools import setup

setup(
    name='random-ansible-host',
    version='0.1',
    py_modules=['random_ansible_host'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        rah=random_ansible_host:cli
    ''',
)
