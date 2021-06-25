import requests
import json
from progress.bar import ChargingBar
import random
import pathlib


class IssueReport(object):



    def __init__(self, repo_name: str, repo_owner: str, state="CLOSED"):


        with open(pathlib.Path("auth/github-api-token.json")) as json_file:
            js = json.load(json_file)
            # if js['TOKEN'] == "enter your token here":
            #     raise Exception("Please enter ")

        #Ignore: use this path if testing within a python IDE

        # with open(pathlib.Path("../auth/github-api-token.json")) as json_file:
        #     js = json.load(json_file)

        self.repo_name = repo_name
        self.repo_owner = repo_owner
        self.state = state
        self.report = []
        self.num_issues = 0
        self.headers = {"Authorization": "Bearer {}".format(js['TOKEN'])}
        self.__execute_request()

    def get_report(self):
        return self.report

    def __issue_count_template(self, quantity = 100, cursor = 100) -> str:
        q = """
            query {{
                repository(owner: "{}", name: "{}") {{
                    issues(last: 0, states:{}) {{
                        totalCount
                    }}
                }}
            }}""".format(self.repo_owner, self.repo_name, self.state)
        return q

    def __initialize_pagination_template(self, quantity: int, cursor: str) -> str:
        q = """
            query {{
                repository(owner: "{}", name: "{}") {{
                    issues(last: 1, states:{}) {{
                      edges {{
                        cursor
                      }}
                    }}
                }}
            }}""".format(self.repo_owner, self.repo_name, self.state)
        return q

    def __report_template(self, quantity: int, cursor: str) -> str:
        q = """
            query {{
                repository(owner: "{}", name: "{}") {{
                    issues(last: {}, before: "{}", states:{}) {{
                      edges {{
                        cursor
                        node {{
                          number
                          url
                          title
                          createdAt
                          comments {{
                            totalCount
                          }}
                          labels(first: 10) {{
                            edges {{
                              node {{
                                name
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                }}
            }}""".format(self.repo_owner, self.repo_name, quantity, cursor, self.state)
        return q

    def __simple_report_template(self, quantity: int, cursor: str) -> str:
        q = """
            query {{
                repository(owner: "{}", name: "{}") {{
                    issues(last: {}, states:{}) {{
                      edges {{
                        cursor
                        node {{
                          number
                          url
                          title
                          createdAt
                          comments {{
                            totalCount
                          }}
                          labels(first: 10) {{
                            edges {{
                              node {{
                                name
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                }}
            }}""".format(self.repo_owner, self.repo_name, quantity, self.state)
        return q

    def __issue_count(self, issue_json: dict) -> int:
        # print(issue_json)
        r = issue_json['data']['repository']['issues']
        self.num_issues = r['totalCount']
        return self.num_issues

    def __process_issue_request(self, issue_json: dict) -> list:
        r = issue_json['data']['repository']['issues']['edges']
        result = [
            {
                'cursor': value['cursor'],
                **value['node'],
                'number': int(value['node']['number']),
                'issue title': value['node']['title'],
                'issue created at': value['node']['createdAt'],
                'comments': value['node']['comments']['totalCount'],
                'labels': ", ".join(x['node']['name'] for x in value['node']['labels']['edges']),
                'repo owner': self.repo_owner,
                'repo name': self.repo_name
            }
            for value in r
        ]
        return result

    def __post_request(self, query_template, quantity = 100, cursor =""):
        request = requests.post('https://api.github.com/graphql', json={'query': query_template(quantity, cursor)}, headers=self.headers)
        if request.status_code == 401:
            raise Exception("Please enter your valid authorization token in auth/github-api-token!")
        elif request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query_template(self, quantity, cursor)))

    def __execute_request(self):
        num_r = self.__post_request(self.__issue_count_template)
        iss_count = self.__issue_count(num_r)
        resultant = []
        if iss_count != 0:
            if iss_count > 100:
                bar = ChargingBar(' Report Loading ', suffix='%(percent)d%%', max=(round(iss_count/100)))
                pagination_r = self.__post_request(self.__initialize_pagination_template)
                v = pagination_r['data']['repository']['issues']['edges']
                cursor = v[0]['cursor']
                i = iss_count
                while i / 100 > 1:
                    i = i - 100
                    request = self.__post_request(self.__report_template, 100, cursor)
                    t = self.__process_issue_request(request)
                    cursor = t[0]['cursor']
                    for issues in t:
                        if isinstance(issues, dict):
                            resultant.append(issues.copy())
                    # print("Report Loading: " + str(round(((len(resultant) / iss_count) * 100))) + "% \n")
                    bar.next()
                request = self.__post_request(self.__report_template, 100, cursor)
                t = self.__process_issue_request(request)
                for issues in t:
                    if isinstance(issues, dict):
                        resultant.append(issues.copy())
                bar.finish()
                print(" \nReport Completed Successfully: {} Issues Found".format(len(resultant)))
                self.report = resultant.copy()
                return resultant
            else:
                request = self.__post_request(self.__simple_report_template)
                t = self.__process_issue_request(request)
                print(" \nReport Completed Successfully: {} Issues Found".format(len(t)))
                self.report = t.copy()
                return t

    def filter_by_comments(self, min_comments):
        report_copy = self.report.copy()
        for value in self.report:
            if value['comments'] < min_comments:
                report_copy.remove(value)
        self.report = report_copy.copy()
        print("Returning {} Issues with more than {} comments".format(len(self.report), min_comments))

    def get_sample_report(self, sample_amount: int) -> list:
        n = sample_amount
        samp_report = []
        if sample_amount > self.num_issues:
            raise Exception("Requested sample size of {} is larger than report size. Please try again with a sample size below {}".format(sample_amount, self.num_issues))
        else:
            samp_report = random.sample(self.report, round(n))
            print("Sampling Successful: {} Issues Sampled".format(sample_amount))
        return samp_report

if __name__ == '__main__':
    # report = IssueReport(repo_name="yolov5", repo_owner="ultralytics")
    report = IssueReport(repo_name="FastMaskRCNN", repo_owner="CharlesShang").get_report()
    print(report)

    # df = pd.DataFrame(report)
    # print(report)

# df = pd.DataFrame(report)
# print(df.head())
