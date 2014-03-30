from setuptools import setup

setup(
    name='secret-manager',
    version='0.0.1a',
    description='Simple GPG powered secret manager.',
    url='https://github.com/winny-/secret-manager',
    author='Winston Weinert',
    author_email='winston@ml1.net',
    license='MIT',
    packages=['secret_manager'],
    test_suite='secret_manager.test',
    )
