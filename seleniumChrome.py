from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Open Jenkins
driver.get("http://google.com")
assert "Google" in driver.title

# Login Jenkins
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("Hello World")
elem.send_keys(Keys.ENTER)
assert "Hello World" in driver.title

#Open new Tab
driver.execute_script('''window.open("http://google.com", "_blank");''');
tabs = driver.window_handles
print (tabs)
assert "Google" in driver.title

# Go back to Initial tab
#driver.switch_to_window(tabs[0])


#driver.close()
