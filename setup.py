from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='github-trending-api',
    version='0.2.1',
    description='Pypi package to access Github trending in Python',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Manjot Pahwa',
    author_email='manjot.pahwa@gmail.com',
    keywords=['Github', 'Github Trending'],
    url='https://github.com/manjotpahwa/github-trending-api',
    download_url='https://pypi.org/project/github-trending-api/'
)

install_requires = [
    'aiohttp',
    'lxml'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
