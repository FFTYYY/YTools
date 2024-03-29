from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('LICENSE', encoding='utf-8') as f:
    license = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    reqs = f.read()

pkgs = [p for p in find_packages() if p.startswith('YTools')]
print(pkgs)

setup(
    name='YYYTools',
    version='0.1.16',
    url='http://github.com/FFTYYY/YTools',
    description='',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    author = 'Yongyi Yang',
	author_email = 'yongyi@umich.edu',
    python_requires = '>=3.6',
    packages = pkgs,
    install_requires = reqs.strip().split('\n'),

    include_package_data = True , 
)