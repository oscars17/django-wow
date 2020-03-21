import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='django-wow',
    version='0.0.3',
    packages=['django_wow',
              'django_wow.community',
              'django_wow.oauth2'],
    description='API Wrapper',
    author='Oscars17',
    author_email='oscar.s1733@gmail.com',
    url='https://github.com/oscars17/django-wow',
    install_requires=['requests', 'requests_oauthlib'],
    python_requires='>=3.6',
)
