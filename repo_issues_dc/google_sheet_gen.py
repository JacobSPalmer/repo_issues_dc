from datetime import date
from google.oauth2 import service_account
from googleapiclient.discovery import build
import numpy as np
from repo_issues_dc import IssueReport as IR
import pandas as pd
import pathlib



credentials = service_account.Credentials.from_service_account_file(
    str(pathlib.Path("auth/issue-report-generation-ff9748b57ae2.json"))
)

#Ignore unless working within an IDE
# credentials = service_account.Credentials.from_service_account_file(
#     str(pathlib.Path("../auth/issue-report-generation-ff9748b57ae2.json"))
# )

scopes = credentials.with_scopes(
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
)

def create_sheet(title, repo_name, repo_owner, data):
    sheets_service = build("sheets", "v4", credentials=credentials)
    sheets = sheets_service.spreadsheets()

    # create_body = {"properties": {"title": f"{title} {date.today()}"},
    #                "sheets": list(map(lambda d: {"properties": {"title": d.get("title")}}, data))}
    create_body = {"properties": {"title": f"{title}: {repo_owner}/{repo_name}"},
                   "sheets": list(map(lambda d: {"properties": {"title": d.get("title")}}, data))}
    res = sheets.create(body=create_body).execute()
    spreadsheet_id = res.get("spreadsheetId")

    def df_to_sheet(df):
        df_columns = [np.array(df.columns)]
        df_values = df.values.tolist()
        df_to_sheet = np.concatenate((df_columns, df_values)).tolist()
        return df_to_sheet

    update_body = {
        "valueInputOption": "RAW",
        "data": list(map(lambda d: {"range": d.get("title"), "values": df_to_sheet(d.get("df"))}, data))
    }

    sheets.values().batchUpdate(spreadsheetId=spreadsheet_id, body=update_body).execute()
    return res

def share_spreadsheet(spreadsheet_id, options, notify=False):
    drive_service = build("drive", "v3", credentials=credentials)
    res = (
        drive_service.permissions()
        .create(
            fileId=spreadsheet_id,
            body=options,
            sendNotificationEmail=notify,
        )
        .execute()
    )
    return res

def generate_spreadsheet_link(issue_list: list) -> str:
    df = pd.DataFrame(issue_list)
    # df = df[['repo owner', 'repo name','issue ID', 'url','issue created at', 'labels', 'comments']]
    df = df[['issue ID', 'url', 'labels', 'comments', 'created at', 'repo owner', 'repo name']]

    data = [
        {
            "title": "Issues",
            "df": pd.DataFrame(df)
        }
    ]
    options = {
        "role" : "reader",
        "type": "anyone"
    }
    repo_name = issue_list[0]['repo name']
    repo_owner = issue_list[0]['repo owner']
    res = create_sheet("Report Sheet", repo_name = repo_name, repo_owner = repo_owner, data=data)
    share = share_spreadsheet(res.get("spreadsheetId"), options=options)
    print(" Generated Google Sheets Link: " + res.get("spreadsheetUrl"))
    return res.get("spreadsheetUrl")



