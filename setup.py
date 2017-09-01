from setuptools import setup, find_packages

setup(
	name='CS_Tool',
	version='1.0',
	packages=find_packages(),
	scripts=['app.py'],
	
	install_requires=['peppercorn'],
	python_requires='>=3',
	
	author="Pieter",
	author_email="pieter_gilissen@hotmail.com",
	description='A CS analysis tool for LOL',
	url='https://github.com/TeamMoodGitHub/Pieter-Term-1',
	classifiers=[
	'Development Status :: 3 - Alpha',
	'Inteded Audience :: League Players',
	'Programming Language :: Python :: 3.6',
	],
	#packages=['flask','matplotlib','numpy','requests','pickle','pillow']
	)
