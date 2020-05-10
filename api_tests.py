#!/usr/bin/env python3

from test_p2api import P2ApiTest


def report_results(test_case_id, results):
    print(f'Test results for {test_case_id}:')
    passed = True
    for result in results:
        if 'P' in result:
            print(f"Step passed: {result['P']}")
        elif 'F' in result:
            passed = False
            print(f"Step failed: {result['F']}")

    print(f'Overall test result for {test_case_id}: '
          f'{"Pass" if passed else "Fail"}')


# Similar comment to the selenium tests regarding regarding
# importing/updating tests in a database from test specs e.g yaml files
# then running the tests in the database and recording the results in the
# database

tester = P2ApiTest()

# Happy path
results = tester.run_test_case('fc_test_001', 'test.jpg', 1, 204)
report_results('fc_test_001', results)

# FC out of range 400
results = tester.run_test_case('fc_test_002', 'test.jpg', 0, 400)
report_results('fc_test_002', results)

# FC out of range 400
results = tester.run_test_case('fc_test_003', 'test.jpg', 6, 400)
report_results('fc_test_003', results)

# FC doesn't exist 404
results = tester.run_test_case('fc_test_004', 'test.jpg', 5, 404)
report_results('fc_test_004', results)

# TODO other test cases
# 400: Submitted information incorrect
# Need to allow test case to change authentication just for the delet call
# 401: Not authenticated
# Need a user without permissions to delete FCs
# 403: No permission (Not sure if we can do this)
# 409: Not sure how to test this "The OB must first be migrated to the
# latest instrument package." Presumably we need an OB created in some
# other way
