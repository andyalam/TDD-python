from selenium import webdriver
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

        #Check the page title
        self.assertIn('To-Do', self.browser.title)

        self.fail('Finish the test!')

        # The user is invited to enter a to-do item right away

        # The user types "Download more RAM" into a text box

        # When the user hits enter, the page updates, and now
        # the to-do item "Download more RAM" is added to the to-do list

        # The user is invited to enter another to-do item via text box
        # The user enters "Download a car"

        # The page udpates again and shows the new to-do-item
        # added to the list

        # The user notices that the URL has been changing, presumably to
        # save his/her list in the URL.

        # The user revisits that URL, the list is still there, 'saved'.

        # The user leaves the site.

if __name__ == '__main__':
    unittest.main()
