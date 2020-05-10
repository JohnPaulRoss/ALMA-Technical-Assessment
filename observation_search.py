""" Provides a mean of performing a search """
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

DEFAULT_WAIT = 60
WAIT_FOR_SEARCH_RESULTS = 10


class ObservationSearch():

    def __init__(self, url, user_agent):
        # TODO add headless parameter could
        # actually change the browser
        # but just changing the useragent
        # should be sufficient
        profile = webdriver.FirefoxProfile()
        if user_agent:
            profile.set_preference(
                'general.useragent.override', user_agent)
        self.driver = webdriver.Firefox(profile, executable_path='geckodriver')
        self.url = url
        # Wait if an element isn't immediately there
        # Save lots of horrible exception handling but
        # might affect test performance and might result
        # in incorrect test failures.
        self.driver.implicitly_wait(DEFAULT_WAIT)

    def __del__(self):
        self.driver.quit()

    def set_search_criteria(self, field_id, field_value):

        # Scroll into view by hovering over the search button

        try:
            search_button_element = self.driver.find_element_by_id(
                'search-button')
            hover = ActionChains(self.driver).move_to_element(
                search_button_element)
            hover.perform()
        except NoSuchElementException:
            return ({'F': 'Could not find search button. Unable to run test'},
                    False)

        try:
            element = self.driver.find_element_by_id(field_id)
            element.click()
            element.clear()
            element.send_keys(field_value)
        except NoSuchElementException:
            return ({'F': ('Could not find specified search field. '
                           'Unable to run test')}, False)
        return ({'P': 'Successfully set search criteria'}, True)

    def count_observation_panel_elements(self):
        ''' Count returned search results
        '''
        # Don't want to wait for these elements.
        self.driver.implicitly_wait = 0
        elements = self.driver.find_elements_by_xpath(
            f'//*[@id="observation-panel"]/app-table-container/'
            f'app-table/ngx-datatable/div/'
            f'datatable-body/datatable-selection/'
            f'datatable-scroller/'
            f'datatable-row-wrapper')

        self.driver.implicitly_wait = 30

        count = 0
        # Ensure they are displayed
        # probably not necessary but won't hurt
        for el in elements:
            if el.is_displayed():
                count += 1

        return count

    def do_observation_search(
            self,
            field_id=None,
            field_value=None,
            minimum_results=None,
            maximum_results=None):
        """ Performs a search of using field_id and field_value and verifies
        minimum maximum number of search results if specified
        # TODO we could check that the search results actually match
        # the search criteria.
        # Note this test uses existing data and does not change anything
        # so there are no setup or teardown functons. Potentially this
        # will be needed so TODO need to have a mechanism for it.
        """
        self.driver.get(self.url)
        field_id = 'search-input-mous' if field_id is None else field_id
        field_value = 'uid://A002/X639a2a/X2a'\
            if field_value is None else field_value
        minimum_results = 1 if minimum_results is None else minimum_results
        maximum_results = 1 if maximum_results is None else maximum_results
        step_results = []
        r, cont = self.set_search_criteria(field_id, field_value)
        step_results.append(r)

        if not cont:
            return step_results

        # Give the page a chance to update
        sleep(WAIT_FOR_SEARCH_RESULTS)
        count = self.count_observation_panel_elements()
        if minimum_results:
            if count < minimum_results:
                step_results.append({
                    'F': (f'Expected at least {minimum_results}, got '
                          f'{count} in observation panel')})
                return step_results
        if maximum_results:
            if count > maximum_results:
                step_results.append({
                    'F': (f'Expected no more than {maximum_results}, got '
                          f'{count} in observation panel')})
                return step_results
        step_results.append({
            'P': f'observation panel contained {count} results'})

        return step_results
