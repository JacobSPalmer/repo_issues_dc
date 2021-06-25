from repo_issues_dc import IssueReport
from repo_issues_dc import google_sheet_gen

def create_report(owner, name):
    return IssueReport.IssueReport(owner, name)

def generate_spread(report_list):
    return google_sheet_gen.generate_spreadsheet_link(report_list)




