from selenium import webdriver

browser = webdriver.Firefox()

# The user opens the URL of the site
browser.get('http://localhost:8000')

# The homepage title must have 'To-Do' in it somewhere
assert 'To-Do' in browser.title

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
browser.quit()
