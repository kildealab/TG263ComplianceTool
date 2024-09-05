from setuptools import setuptools

# add readme/requirements

setup(
	name="rtstruct-tg263",
	author="Kayla O'Sullivan-Steben",
	author_email="kayla.osullivan-steben@mcgill.mail.ca",
	version='0.1',
	# description='TO DO: add description',
	# packages=['TO DO: add dependences'],
	entry_points = {
		'console_scripts': [
			'find-names=.find_names:main',
			'rename-structures=rename_structures:main'
		]
	}
)
