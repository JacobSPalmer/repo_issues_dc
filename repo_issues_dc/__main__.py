import argparse
import webbrowser
import repo_issues_dc

def main():
    parser = argparse.ArgumentParser(
        'issuereport',
        description='create an issue report for a repository'
    )

    parser.add_argument(
        'owner',
        help="The name of the repository owner",
        type=str,
    )
    parser.add_argument(
        'repo_name',
        help="The name of the repository",
        type=str,
    )
    parser.add_argument(
        '-sample_amount',
        required=False,
        help="Number of issues to randomly sample from the issue report",
        type=int,
        default=0,
    )
    parser.add_argument(
        '-min_comments',
        required=False,
        help="Filters report for all issues with at least the specified minimum amount of comments",
        type=int,
        default=0,
    )
    parser.add_argument(
        '-sample_percent',
        required=False,
        help="Percentage of issues to randomly sample from the issue report",
        type=int,
        default=0,
    )
    args = parser.parse_args()

    if args.sample_amount != 0 and args.sample_percent != 0:
        raise Exception("Cannot sample by percent and amount. Please only specify either percent or amount.")

    report = repo_issues_dc.create_report(args.owner, args.repo_name)

    if args.min_comments > 0:
        report.filter_by_comments(args.min_comments)

    if args.sample_amount == 0 and args.sample_percent == 0:
        link = repo_issues_dc.generate_spread(report.get_report())
        webbrowser.open_new(link)
    elif 0 < args.sample_percent <= 100:
        link = repo_issues_dc.generate_spread(report.get_sample_report_percent(args.sample_percent))
        webbrowser.open_new(link)
    elif args.sample_amount > 0:
        link = repo_issues_dc.generate_spread(report.get_sample_report(args.sample_amount))
        webbrowser.open_new(link)
    else:
        raise Exception("Invalid sample amount or sample percent.")

main()
