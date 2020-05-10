#!/usr/bin/env python3
import argparse
from observation_search import ObservationSearch
from user_agent import generate_user_agent, InvalidOption


def arg_parser():
    # TODO it would be better to pass test vectors and cases
    # using a test specification e.g. by creating some sort
    # of test schema yaml/json which the framework reads and
    # acts upon.
    parser = argparse.ArgumentParser(
        description="Run some selenium tests")
    parser.add_argument(
        '--browser', type=str,
        help='specify the required browser. Valid values are '
             'firefox, chrome, ie')

    parser.add_argument(
        '--field-id', type=str,
        help='Specifies field to search on (default search-input-mous)')

    parser.add_argument(
        '--field-value', type=str,
        help='Specifies the value to use for the field')

    parser.add_argument(
        '--minimum-results', type=int,
        help='Minimum number of search results')

    parser.add_argument(
        '--maximum-results', type=int,
        help='Maximum number of search results')

    parser.add_argument(
        '--platform', type=str,
        help='Specifies a platform to use. '
             'Valid values are win, linux, '
             'mac, android')

    parser.add_argument(
        '--device-type', type=str,
        help='Specifies the device type. '
             'Valid values are smartphone, '
             'desktop or tablet')

    # TODO this needs thought as commented earlier
    # if the framework is to support different types of
    # test using the command line is probably not the
    # best way of doing this.
    parser.add_argument(
        '--test-type', type=str,
        help='Type of test to run (default ob-search)')

    parser.add_argument(
        '--url', type=str,
        help='Url to start at for the test '
        '(default https://almascience.eso.org/asax)')

    args = parser.parse_args()
    return args


args = arg_parser()

url = args.url if args.url else 'https://almascience.eso.org/asax'
browser = args.browser.lower() if args.browser else 'firefox'
platform = args.platform.lower() if args.platform else 'linux'
try:
    user_agent = generate_user_agent(
        os=platform,
        navigator=browser)
    print(user_agent)
except InvalidOption:
    print('Unable to generate user-agent for specified options '
          f'browser={browser}, platform={platform}. Using default')
    user_agent = None

ob_search = ObservationSearch(url, user_agent)

# TODO Results should go in a db for automatic report
# generation and historical records.
test_step_results = ob_search.do_observation_search(
    field_id=args.field_id,
    field_value=args.field_value,
    minimum_results=args.minimum_results,
    maximum_results=args.maximum_results)

print("Test results:")
passed = True
for result in test_step_results:
    if 'P' in result:
        print(f"Step passed: {result['P']}")
    elif 'F' in result:
        passed = False
        print(f"Step failed: {result['F']}")

print(f'Overall test result {"Pass" if passed else "Fail"}')
