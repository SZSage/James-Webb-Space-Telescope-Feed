Nebula Net Interactive Feed Project README


1. System Description:

The Nebula Net Interactive Feed (NNIF) is a web-based platform designed to provide users with access to images captured by the James Webb Space Telescope (JWST). 
Hosted on local servers, the website offers two primary web pages: 
a landing page displaying the latest released photos and meatadata showcasing comprehensive mission information sourced from the NASA JWST website. 
Users can interact with the website to view, download, and explore JWST photos and mission data.

2. Authors:

    Cortez, Isabella
    Burke, Jacob
    Lopez, Freddy
    Willard, Daniel
    Zhao, Simon

3. Creation Date:

NNIF was created on March 12, 2024.

4. Purpose:

The Nebula Net project was developed as a capstone project for CS422 Software Methodology at the University of Oregon. 
It aims to provide a platform for users to access and explore JWST mission data and imagery.

5. Compilation and Execution

see instatation insturctions

6. Additional Setup:

see instatation insturctions

7. Dependencies:

Ensure that the following software dependencies are installed:

    Python v3.11.6
    SQLite3
    Pip (Python Package Manager) (latest version available)
    Python Libraries: 
	Astroquery 
	Astropy 
	Matplotlib 
	Numpy 
	Pandas 
	Beautifulsoup 
	Requests 
	Pytest

8. Directory Structure:

    Documentation/: Contains project documentation.
    WebScraping/: Contains web scraping Python scripts and SQL database.
    nebulanet/: Contains web files and the compiled website through React.
    fetch_process/: Contains scripts for pulling and compiling photos and metadata from JWST.
