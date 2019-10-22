# KPI Web Scraper

Uses an automated browser to access key performance indicator data from an internal web interface and export the metrics to csv.

## Getting Started

To run the KPI scraper, first edit the Scraper Configuration file to include, your login details for pdsm, the url of your table of catalog tasks in EPDSM, and the desired name for the output csv. From here you can run the PDSM_KPI_Scraper exe file. If you run into any errors while running the scraper you may edit the runtime options to allow more time for pages to load depending on your connection speed.

### Prerequisites

To run the scraper you must have access to a EPDSM account, as well as its login details.  

### Installing

No Installation required, just download the exe, configure the Scraper_Configuration file and run. :)

## Built With

* Python - The programming language used
* Selenium - Webdriver Automation
* Beautiful Soup - Used to analyze and organize html
* Pandas - Used to export data to csv
* PyInstaller - Used to convert distribution to executable format 
