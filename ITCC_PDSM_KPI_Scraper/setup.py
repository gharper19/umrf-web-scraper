"""
Packaging and Distribution Options:
1) Requires Python Install - Offline dependency install-from-dir -  https://stackoverflow.com/questions/36725843/installing-python-packages-without-internet-and-using-source-code-as-tar-gz-and
		- Same with webdriver offline install - https://stackoverflow.com/questions/52861370/how-can-i-package-and-distribute-python-projects-with-dependencies-that-require
2) 

"""

import sys
from cx_Freeze import setup, Executable

build_exe_options= {
	"packages": [],
	"excludes": []
}

base = None

setup( name = "PDSM KPI Scraper", 
		version= "0.1",
		description= "Scrapes KPI Data on PDSM for ITCC",
		options= {"build_exe": build_exe_options}, 
		executables = [Executable("PDSM_KPI_Scraper.py", base=base)]
		# options
    	# install_requires = ['selenium'],
		)