from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        #The user opens the site
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Download more RAM' for row in rows),
            "New to-do item did not appear in table"
        )

        # The user is invited to enter another to-do item via text box
        # The user enters "Download a car"
        self.fail('Finish the test!')

        # The page udpates again and shows the new to-do-item
        # added to the list

        # The user notices that the URL has been changing, presumably to
        # save his/her list in the URL.

        # The user revisits that URL, the list is still there, 'saved'.

        # The user leaves the site.

if __name__ == '__main__':
    unittest.main()
