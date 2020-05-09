import json
import requests
import p2api


class P2ApiTest():

    # TODO consider improving this class to make it more generic
    # Or have a base class and the more specialised classes for
    # different types of tests
    def __init__(self):
        self.CONTAINER_ID = 1448455
        # Wouldn't be needed if we were using the api throughout
        # See comments around its use
        self.api = p2api.ApiConnection('demo', 52052, 'tutorial')
        # TODO Consider a way of hiding this
        self.P2API_SECRET_DATA = {"username": "52052", "password": "tutorial"}
        self.P2API_BASE_URL = "https://www.eso.org/copdemo/api/"

    def get_access_code(self):
        response = requests.post(
            f'{self.P2API_BASE_URL}login', self.P2API_SECRET_DATA)

        if response.status_code in [200]:
            token_dict = json.loads(response.text)

        if 'token_type' in token_dict:
            token_type = token_dict['token_type']
        else:
            return False

        if 'access_token' in token_dict:
            access_token = token_dict['access_token']
        else:
            return False

        return f'{token_type} {access_token}'
        # TODO Consider whether we need the to use the refresh token
        # Probably not for short lived tests

    def create_ob(self, container_id, text):

        # Create observing block
        # api_call_headers = {'Authorization': self.token}

        # api_call_body = {
        #    "itemType": "OB",
        #    "name": text}

        # url in spec was wrong (v1)
        # api_call_url = f'{P2API_BASE_URL}v1/containers/{container_id}/items'
        # Create an observing block use idempotent call
        # This resulted in a 500 error
        # {"error":"Oops, java.lang.IllegalStateException: getReader()
        # has already been called for this request"}
        # Note, this may have been caused by previous erroneous calls
        # Try to repeat on a different container at some point.
        # response = requests.put(
        #    api_call_url, api_call_body, headers=api_call_headers)
        # print(response.text)
        # print(response.status_code)

        # Since create api seems to be at least partly broken create
        # an ob using p2api we are not testing this part of the api
        # In the real world report this api fault.
        return self.api.createOB(container_id, text)

    def add_fc(self, ob_id, filename):

        # TODO Consider using api but we are
        # not currently testing this part of the api
        self.api.addFindingChart(ob_id, filename)
        return self.api.getFindingChartNames(ob_id)

    def setUp(self):
        self.token = self.get_access_code()

    def tearDown(self, ob_id, observation):
        # TODO needs expanding to be more robust
        # Ideally make it a generic teardown
        self.api.deleteOB(ob_id, observation)

    def run_test_case(
            self,
            test_case_id,
            fc_file,
            index,
            expected_status_code):
        self.setUp()
        test_results = []

        ob, observation = self.create_ob(
            self.CONTAINER_ID, f"Ob for {test_case_id}")
        if 'obId' not in ob:
            test_results.append(
                {'F': f'Could not create ob for {self.CONTAINER_ID}'})
            return test_results
        else:
            test_results.append(
                {'P': f'Successfully created ob for {self.CONTAINER_ID}'})
        ob_id = ob['obId']

        if self.add_fc(ob_id, fc_file):
            test_results.append(
                {'P': f'Successfully created finding chart'})
        else:
            test_results.append(
                {'F': f'Failed to create finding chart'})
            return test_results

        url = (f'{self.P2API_BASE_URL}v1/obsBlocks/{ob_id}'
               f'/findingCharts/{index}')
        headers = {
            'Authorization': self.token,
            'Content-Disposition': f'inline; filename={fc_file}',
            'Content-Type': 'image/jpeg'}
        print(url)
        response = requests.delete(url, headers=headers)
        print(response.content)
        if response.status_code != expected_status_code:
            test_results.append(
                {'F': f'Expected status code {expected_status_code} '
                      f'got {response.status_code}'})
        else:
            test_results.append(
                {'P': f'Got the expected status code {expected_status_code}'}
            )
        self.tearDown(ob_id, observation)
        return test_results
