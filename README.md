# Training Certificate Expiration: AI Tracker and Email Notification

Intro summary...

## Installation and Setup

This project uses Python and Conda for environment management

### Prerequisites
- Miniconda or Anaconda

### Setup
 1. Clone the repo
 'git clone https://github.com/andrea-fung/expiry-tracker.git'

 2. Create the Conda environment

 Go to your repository.
 If using Minicoda/Anaconda, run: 
 'conda env create -f environment.yml'
 'conda activate cert_tracker'

 Otherwise, install libraries with the requirements.txt file and activate virtual environment.

 3. Create an .env file 
    - write 'GMAIL_PASS='[YOUR_PASS_TOKEN]'' 
    - if not using gmail for sending email notification, create an alternative password and modify the send_email function in main.py as appropriate.

 4. create a data folder at the root folder
 5. Modify `src/cert_tracker/crews/cert_tracker_crew/config/constants.yaml` to define your data paths and preferences.
 6. For Sharepoint/OneDrive folder updating
    - Sync OneDrive folder to your local system
    - Create a Microsoft PowerAutomate flow 
    - In the OneDrive folder, create a FlowTrigger and FlowData folder

## Running the Project

To kickstart your flow and begin execution, run this from the src folder of your project:
'python3 -m cert_tracker.main'

