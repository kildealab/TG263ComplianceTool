from setuptools import setup, find_packages

# add readme/requirements

setup(
	name="rtstruct-tg263",
	author="Kayla O'Sullivan-Steben",
	author_email="kayla.osullivan-steben@mcgill.mail.ca",
	version='0.1',
	# description='TO DO: add description',
	packages=find_packages(),
	entry_points = {
		'console_scripts': [
			'find-names=scripts.find_names:main',
			'rename-structures=scripts.rename_structures:main'
		]
	}
)
