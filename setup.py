from setuptools import setup, find_packages

setup(
    name='pmserializer',
    version="1.0.1",
    description="serializer of few formats",
    author="Carcajo",
    author_email='t375445391507@gmail.com',
    install_requires=["pytomlpp", 'pyyaml'],
    packages=find_packages(),
    test_suite='tests/',
)
