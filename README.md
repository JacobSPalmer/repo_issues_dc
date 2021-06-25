# Repository Issue Report
Tool to automatically gather and format information from GitHub repository issues for analysis

## Getting Started:
To get started, generate a GitHub Authorization Token. Following, download the project and open the github-api-token.json file found in the auth folder. Copy and paste your GitHub token where stated.

Ensure that all required packages are installed within the requirements.txt.

## To Run:
Navigate to the project folder within terminal/console and run the following command using python:

`python -m repo_issues_dc [name of repository] [owner username of repo]`

Optionally, you can filter by comments using:

`python -m repo_issues_dc [name of repository] [owner username of repo] -min_comments [minimum number of comments]`

As well as return a number of randomly sampled issues (can also be used with filter by comments):

`python -m repo_issues_dc [name of repository] [owner username of repo] -sample_amount [# of issues to sample]`

The result will generate a google sheets page and automatically open in your default browser. You can save a copy to your Google Drive from here if desired.
