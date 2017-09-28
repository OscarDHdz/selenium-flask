from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Open Jenkins
driver.get("http://localhost:8080")
assert "Jenkins" in driver.title

# Login Jenkins
elem = driver.find_element_by_name("j_username")
elem.clear()
elem.send_keys("admin")
elem = driver.find_element_by_name("j_password")
elem.clear()
elem.send_keys("admin")
elem.send_keys(Keys.ENTER)
assert "Dashboard" in driver.title

#Open new Tab
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
driver.execute_script('''window.open("http://localhost:8080/blue/pipelines", "_blank");''');
#assert "New Tab" in driver.title
tabs = driver.window_handles
print (tabs)
assert "Jenkins" in driver.title

# Go back to Initial tab
driver.switch_to_window(tabs[1]) 


#driver.close()