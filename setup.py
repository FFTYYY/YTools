from setuptools import setup


with open('requirements.txt', encoding='utf-8') as f:
	reqs = f.read()

setup(
	name = 'YYYTools',
	version = '0.1',
	description = '',
	url = 'http://github.com/FFTYYY/YYYTools',
	author = 'Yang Yongyi',
	author_email = '1004473299@qq.com',
	license = 'MIT',
	packages = ['YYYTools'],
	zip_safe = False,
    install_requires = reqs.strip().split('\n'),
)