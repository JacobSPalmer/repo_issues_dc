# Repository Issue Report
Tool to automatically gather and format information from GitHub repository issues for analysis

## Getting Started:

### Authorization
To get started, generate a GitHub Authorization Token. Go to *Settings > Developer settings > Personal access tokens* and click *Generate new token*.
Here are the minimum scopes to select when creating the key:

[Personal Access Token Scopes](https://i.imgur.com/QaTvgwk.jpg)

Following that, download the project and open the github-api-token.json file found in the auth folder. Copy and paste your GitHub token where stated and save the file.

You do not need to change the file titled *issue-report-generation-ff9748b57ae2.json*. This is a auth file to allow for Google Sheets integration.

### Project Requirements

Ensure that all required packages are installed within the requirements.txt. I'd recommend creating a environment within Anaconda and then install the packages within that environment by opening a command terminal within the environment, navigate the project root directory, and run the following command:

`pip install -r requirements.txt`

## To Run:
Navigate to the project folder within terminal/console and run the following command using python:

`python -m repo_issues_dc [name of repository] [owner username of repo]`

Optionally, you can filter by comments using:

`python -m repo_issues_dc [name of repository] [owner username of repo] -min_comments [minimum number of comments]`

As well as return a number of randomly sampled issues (can also be used with filter by comments):

`python -m repo_issues_dc [name of repository] [owner username of repo] -sample_amount [# of issues to sample]`

The result will generate a google sheets page and automatically open in your default browser. You can save a copy to your Google Drive from here if desired.

## Example Command:

`python3 -m repo_issues_dc yolov5 ultralytics -min_comments 3 -sample_amount 300`

`python3`: refers to my version of python. Depending on your default python system, this could also just be `python` as well (I have python 2 installed and didnt bother changing PATH so python3 refers to it's namesake rather than python 2)

`-m`: is a flag that indicates to run the python module as a script

`repo_issues_dc`: the name of the module and core part of the program. This then refers the program to the __init__ where the argparse can be found and handles the CL input the follows

`yolov5 ultralytics`: this is the specification of the repo to examine. The format is {name of repo} {owner username of repo}. This is case sensitive and must be exact.

`-min_comments 3`: an optional parameter that allows for the issues returned to be filterted by their amount of comments inclusively (issues returned have comments >= specified int)

`-sample_amount 300`: an optional parameter that specifies the number of issues to randomly sampled. If used in unison with min_comments, it will sample from the issues that meet the minimum comment requirement.

## Compatability:

This program has been tested successfully on Windows and Linux systems.
