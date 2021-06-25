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
        type=str,
    )
    parser.add_argument(
        'repo_name',
        type=str,
    )
    parser.add_argument(
        '-sample_amount',
        required=False,
        type=int,
        default=0,
    )
    parser.add_argument(
        '-min_comments',
        required=False,
        type=int,
        default=0,
    )
    args = parser.parse_args()

    report = repo_issues_dc.create_report(args.owner, args.repo_name)

    if args.min_comments > 0:
        report.filter_by_comments(args.min_comments)

    if args.sample_amount > 0:
        link = repo_issues_dc.generate_spread(report.get_sample_report(args.sample_amount))
        webbrowser.open_new(link)
    elif args.sample_amount == 0:
        link = repo_issues_dc.generate_spread(report.get_report())
        webbrowser.open_new(link)
    else:
        raise Exception("Invalid sample amount.")

main()
