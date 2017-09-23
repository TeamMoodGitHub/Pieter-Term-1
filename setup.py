from setuptools import setup, find_packages

setup(
	name='CS_Tool',
	version='1.0',
	packages=find_packages(),
	install_requires=['flask','matplotlib','numpy','requests','pillow'],
	python_requires='>=3',
	author="Pieter",
	author_email="pieter_gilissen@hotmail.com",
	description='A CS analysis tool for LOL',
	classifiers=[
	'Development Status :: 3 - Alpha',
	'Inteded Audience :: League Players',
	'Programming Language :: Python :: 3.6',
	],
	)
