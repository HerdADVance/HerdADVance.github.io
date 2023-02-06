from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
import wget

#driver = webdriver.Chrome('~/Downloads/chromedriver_mac64/chromedriver.exe')
#driver.get('https://www.kenpom.com')

def launchBrowser():
	# chrome_options = Options()
	# chrome_options.binary_location="../Google Chrome"
	# chrome_options.add_argument("start-maximized");
	driver = webdriver.Chrome("~/Downloads/chromedriver_mac64/chromedriver.exe")

	driver.maximize_window()
	driver.get("https://www.kenpom.com")
	WebDriverWait(driver, 10)

	#driver.find_element(By.ID, "content-header")
	#driver.find_element(By.XPATH, "//input[@name='email']").send_keys('abcdef')
	
	#act = ActionChains(driver)
	#act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
	
	team_names = []
	teams = driver.find_elements(By.XPATH, "//table[@id='ratings-table']//tbody//td[@class='next_left']")
	for tn in teams:
		team_names.append(tn.text)

	team_rows = []
	rows = driver.find_elements(By.XPATH, "//table[@id='ratings-table']//tbody//tr")
	for row in rows:
		team_rows.append(row.text)

	output = ""
	for idx, row in enumerate(team_rows):
		output += str(idx + 1) + ','
		output += team_names[idx]

		#team_start_idx = s.find(team_names[idx])
		#end_idx = start_idx + len(team_names[idx])

		after_team_name = row[row.index(team_names[idx]) + len(team_names[idx]):]
		after_team_name = after_team_name.replace(" ", ",")

		output += after_team_name
		output += '\n'
	
	print(output)
	f = open('data/kenpom/test.csv', "w")
	f.write(output)
	f.close()



	#src_elem = driver.find_element(By.ID, "data-area")
	# src_elem = WebDriverWait(driver, 10).until(
	# 	EC.presence_of_element_located((By.ID, "ratings-table"))
 #    )
	#src_elem.click()
	#src_elem.send_keys('abcdef')
	#src_elem.send_keys(Keys.COMMAND + 'a') # select all the text
	#copied = src_elem.send_keys(Keys.COMMAND + 'c')



	#print(copied)
	#src_elem.send_keys(Keys.CONTROL + 'a') # select all the text
	#src_elem.send_keys(Keys.CONTROL + 'c') # copy it

	while(True):
	   pass

	#return driver

launchBrowser()