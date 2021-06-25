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

# credentials = service_account.Credentials.from_service_account_file(
#     str(pathlib.Path("../auth/issue-report-generation-ff9748b57ae2.json"))
# )

scopes = credentials.with_scopes(
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
)

def create_sheet(title, data):
    sheets_service = build("sheets", "v4", credentials=credentials)
    sheets = sheets_service.spreadsheets()

    # Body of create method with a Spreadsheet(https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet) instance
    create_body = {"properties": {"title": f"{title} {date.today()}"},
                   "sheets": list(map(lambda d: {"properties": {"title": d.get("title")}}, data))}
    res = sheets.create(body=create_body).execute()
    spreadsheet_id = res.get("spreadsheetId")

    # Transform the DataFrame into a matrix of the columns and values
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
    df = df[['repo owner', 'repo name','number', 'url','issue created at', 'labels', 'comments']]
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
    res = create_sheet("Report Sheet", data=data)
    share = share_spreadsheet(res.get("spreadsheetId"), options=options)
    print("Generated Google Sheets Link: " + res.get("spreadsheetUrl"))
    return res.get("spreadsheetUrl")


# if __name__ == '__main__':
#     print(pathlib.Path("../auth/github-api-token.json"))
#     # report = IR.IssueReport(repo_name="yolov5", repo_owner="ultralytics")
#     report = IR.IssueReport(repo_name="pytorch-CycleGAN-and-pix2pix", repo_owner="junyanz")
#     sheet = generate_spreadsheet_link(report.get_sample_report(50))

    # print(sheet)
