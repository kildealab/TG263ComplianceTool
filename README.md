# TG263ComplianceTool
The TG263ComplianceTool is designed to ensure compliance with the TG263 standard for DICOM-RT Structure Set files and XML template files. It automates the process of verifying compliance, proposing new structure names, and renaming DICOM and XML files to meet the required naming conventions. 

## Table of Contents
- [Motivation](#Motivation)
- [Features](#Features)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [Contact](#Contact)

## Motivation
TG 263 provides guidelines for standardized naming of radiotherapy targets and anatomical structures. However, a significant portion of existing data does not perfectly comply with the standard, including data produced before the standard was introduced, as well as data produced afterward, as many clinics do not follow by the standard or do not implement it correctly. This inconsistency makes the analysis of these structures challenging, especially when aggregating large datasets for Big Data and AI. Therefore, the TG263ComplianceTool was created to facilitate the verification and renaming of DICOM and XML files exported from the treatment planning system, thereby simplifyinng downstream analysis tasks.

## Features
* **Automated Compliance Checking**: Automatically checks DICOM files or XML templates for compliance with TG263 standards for both target and anatomical structures.
* **New Name Proposal**: Proposes replacement compliant names.
* **File Renaming**: Renames DICOM files and XML templates based on proposed and user-input names.
* **Configurable Settings**: Allows users to configure file types and paths through a config.py file.


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
   Note: the requirements include the line ```-e .```, which installs the current package with editing permissions. This will allow you to call the scripts above, and the ```-e``` flag allows you to edit code in the package without reinstalling.
   

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
To find and check the compliance of the DICOM files or XML templates, run the following command line:
```
find-names
```
This script will produce three csv files:
* **```NAMES_TO_CONVERT.csv```: contains non-compliant structures and proposed new names. This file  must be edited by the user!**
* ```output/unique_list_structs.csv``` : for user's interest, contains both compliant and non-compliant names appearing in the data --> shows each name only once (with number of instances)
* ```output/individual_list_structurs.csv```: for user's interest, contains both compliant and non-compliant names appearing in the data --> shows each individual file and each individual name, with repeats.

### Step 3 - Verify and fill in structure names to be converted
Open the file ```NAMES_TO_CONVERT.csv``` and fill in the blanks where a new name could not be proposed. It is also highly recommended to review the names proposed by the script to ensure that they are correct.
### Step 4 - Run the rename-structure script
To automarically rename the files based on the new names proposed in ```NAMES_TO_CONVERT.csv```, run the following command line:
```
rename-structures
```
The new renamed DICOM and/or XML files will now be in the output directory (or the path specified by the ```save_path``` variable in ```config.py```).
## Contributing
We welcome contributions! If you are interested in contributing, please fork the repository and create a pull request with your changes.
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit them.
4. Push your branch: `git push origin feature-name`
5. Create a pull request.
## Lincense
This project is licensed under the MIT License - see the LICENSE file for details.
## Contact
For support or questions, please email Kayla O'Sullivan-Steben at kayla.osullivan-steben@mail.mcgill.ca.

