# TG263ComplianceTool


## Table of Contents
- [Motivation](#Motivation)
- [Features](#Features)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [Contact](#Contact)

## Motivation

#### Overview of how X works

## Dependencies
* Python >= 3.8
* numpy >= 1.24.4
* pandas >= 2.0.3
* pydicom >= 2.4.4

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/kildealab/TG263ComplianceTool.git
   ```
2. Navigate to the project directory:
   ```
   cd TG263ComplianceTool
   ``` 
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Install the TG263ComplianceTool package (this will allow you to call the scripts):
   ```
   pip install -e .
   ```
   Note: the ```-e``` flag allows you to edit code in the package without reinstalling. However, you can also install it as ``` pip install . ``` if you do not want that functionality.
   

## Usage
### Step 1 - Set up the config.py file
Open `config.py` and replace the 'file_type' variable with either 'xml' (XML) or 'dcm' (DICOM), and replace the 'PATH' variable with the parent path containing the DICOM or XML files you want to rename. These files can be in subdirectories within the parent PATH. Please see comments in `config.py` for an explanation of the other optional variables.
```

config = {
	'file_type':'xml',# or 'dcm'
	'PATH':'/path/to/parent/directory/to/search/',
	'save_path': '' # will default to output directory if left blank.
}
```
### Step 2 - Run the find-names script
Run the following script to find and check the compliance of XXXX, run the following command line:
```
find-names
```
This will produce a XXXX
### Step 3 - Verify and fill in structure names to be converted
Open the file ```NAMES_TO_CONVERT.csv```
### Step 4 - Run the rename-structure script
To rename the files based on the new names proposed in ```NAMES_TO_CONVERT.csv```, run the following command line:
```
rename-structures
```
## Contributing
We welcome contributions! If you are interested in contributing, please fork the repository and create a pull request with your changes.
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them.
4. Push your branch: `git push origin feature-name`
5. Create a pull request.
## Lincense

## Contact
For support or questions, please email Kayla O'Sullivan-Steben at kayla.osullivan-steben@mail.mcgill.ca.

