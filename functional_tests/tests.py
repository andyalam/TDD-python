#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):

        #The user opens the site
        self.browser.get(self.server_url)

        #Check the page title and the header mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The user is invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # The user types "Download more RAM" into a text box
        inputbox.send_keys('Download more RAM')

        # When the user hits enter, the page updates, and now
        # the to-do item "Download more RAM" is added to the to-do list
        inputbox.send_keys(Keys.ENTER)
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Download more RAM')

        # There is still a text box inviting the user to add another item
        # the users enters "Actually install physical RAM".
        # The page udpates again and shows the new to-do-item
        # added to the list.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Actually install physical RAM')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Download more RAM')
        self.check_for_row_in_list_table('2: Actually install physical RAM')


        # ----------- Now a second user comes along to the site -----------


        ## We use a new browser session to make sure that no information
        ## of Use1 is coming through from cookies, etc
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User2 visits the site. There is no sign of User1's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Download more RAM', page_text)
        self.assertNotIn('Actually install physical RAM', page_text)

        # User2 starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy some milk')
        inputbox.send_keys(Keys.ENTER)

        # User2 gets a unique URL for their list
        # Check that it follows our pattern and does not match user1's URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        # Additional check to make sure user2's unique URL has its item and
        # does not match user1's item(s)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Download more RAM', page_text)
        self.assertIn('Buy some milk', page_text)


    def test_layout_and_styling(self):
        # User goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # The input box is centered on the home page
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # The list of items at redirect is also centered
        inputbox.send_keys('testing, going to new page\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
