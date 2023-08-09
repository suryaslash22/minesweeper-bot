## 1 hit random
## 2 check number of surrounding squares, if unflagged = available, flag them all
# 3 if number = flags around, click all neighbors
# 4 if above does not apply
# 5 use probability: arrangements with bomb in square/ total number of arrangements
# 6 if no probability of 0, go back to step 1

def neighbor_finder(x_int, y_int):

	page_html = browser.page_source
	page_soup = soup(page_html, "lxml")
	game_soup = page_soup.find("div",{"id":"game"})

	neighbors = list()
	if x_int - 1 > 0 and y_int - 1 > 0:
		neighbors.append(game_soup.find("div",{"id":str(x_int-1) + "_" + str(y_int-1)}))

	if x_int - 1 > 0:
		neighbors.append(game_soup.find("div",{"id":str(x_int-1) + "_" + str(y_int)}))

	if x_int - 1 > 0 and y_int + 1 < 31:
		neighbors.append(game_soup.find("div",{"id":str(x_int-1) + "_" + str(y_int+1)}))

	if y_int - 1 > 0:
		neighbors.append(game_soup.find("div",{"id":str(x_int) + "_" + str(y_int-1)}))

	if y_int + 1 < 31:
		neighbors.append(game_soup.find("div",{"id":str(x_int) + "_" + str(y_int+1)}))

	if x_int + 1 < 17 and y_int - 1 > 0:
		neighbors.append(game_soup.find("div",{"id":str(x_int+1) + "_" + str(y_int-1)}))

	if x_int + 1 < 17:
		neighbors.append(game_soup.find("div",{"id":str(x_int+1) + "_" + str(y_int)}))

	if x_int + 1 < 17 and y_int + 1 < 31:
		neighbors.append(game_soup.find("div",{"id":str(x_int+1) + "_" + str(y_int+1)}))

	return neighbors

def idify(x):
	random_sq_id = str(x//30 + 1) + "_" + str(x%30 + 1)
	return random_sq_id

def rev_idify(x):
	random_sq_index = (int(x.split("_")[0]) - 1)*30 + int(x.split("_")[1]) - 1
	return random_sq_index

def soup_it():

	sq_soup = list()
	for index in GRID:
		sq_element = browser.find_element(By.ID, idify(index))
		sq_soup.append(soup(sq_element.get_attribute("outerHTML"), "lxml"))

	# instead of souping, find elements then get attribute - outerHTML

	# page_html = browser.page_source
	# page_soup = soup(page_html, "lxml")
	# game_soup = page_soup.find("div",{"id":"game"})

	# all_sq = game_soup.findAll("div",{"class":"square"})
	# sq_soup = all_sq[:480]

	return sq_soup

def smile():

	page_html = browser.page_source
	page_soup = soup(page_html, "lxml")
	game_soup = page_soup.find("div",{"id":"game"})

	if game_soup.find("div",{"id":"face"})["class"][0] == "facesmile":
		return 1

	elif game_soup.find("div",{"id":"face"})["class"][0] == "facedead":
		return 0

	else:
		return 2

GRID = list(range(0,480))
COMPLETED = list()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import csv
import random
import time
from selenium.common.exceptions import ElementNotVisibleException

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--start-maximized')

browser = webdriver.Chrome("../Web Scraping/chromedriver", chrome_options=options, desired_capabilities=capa)
wait = WebDriverWait(browser, 20)

url = "http://www.minesweeperonline.com"

browser.get(url)
time.sleep(10)

# First move

random_sq_index = random.randint(0,479)
random_sq_id = idify(random_sq_index)
random_sq = browser.find_element(By.ID, random_sq_id)
print("Let's start with " + random_sq_id)
random_sq.click()

# Tactic 1

to_flag = list()
to_click = list()
alive = 1
while alive == 1:

	sq_soup = soup_it()

	numbered_sq = list()
	for div in sq_soup:
	    if "open" in div.div["class"][1]:
	            numbered_sq.append(div.div)

	for div in numbered_sq:

			sq_value = int(div["class"][1][-1:])
			if sq_value > 0:

				x_int = int(div["id"].split("_")[0])
				y_int = int(div["id"].split("_")[1])

				sq_neighbors = neighbor_finder(x_int, y_int)
				available = 0

				for neighbor_div in sq_neighbors:
					if "blank" in neighbor_div["class"][1]:
						available += 1

					elif "bombflagged" in neighbor_div["class"][1]:
						sq_value -= 1

				if sq_value > 0 and sq_value == available:
					for neighbor_div in sq_neighbors:
						if "blank" in neighbor_div["class"][1]:
							target_sq_id = neighbor_div["id"]
							to_flag.append(target_sq_id)

					COMPLETED.append(rev_idify(div["id"]))

				else:
					COMPLETED.append(rev_idify(div["id"]))

	if bool(to_flag):
		print("Tactic 1")

		to_flag = list(dict.fromkeys(to_flag))
		for target_sq_id in to_flag:
			target_sq = browser.find_element(By.ID, target_sq_id)
			ActionChains(browser).move_to_element(target_sq).context_click(target_sq).perform()
			print("Flagging " + target_sq_id)
		
	numbered_sq.clear()
	if COMPLETED:
		GRID = [i for i in GRID if i not in COMPLETED]
		COMPLETED.clear()

	# Tactic 2

	sq_soup = soup_it()

	for div in sq_soup:
	    if "open" in div.div["class"][1]:
	            numbered_sq.append(div.div)

	for div in numbered_sq:

			sq_value = int(div["class"][1][-1:])
			if sq_value > 0:

				x_int = int(div["id"].split("_")[0])
				y_int = int(div["id"].split("_")[1])

				sq_neighbors = neighbor_finder(x_int, y_int)
				available = 0

				for neighbor_div in sq_neighbors:
					if "blank" in neighbor_div["class"][1]:
						available += 1

					elif "bombflagged" in neighbor_div["class"][1]:
						sq_value -= 1

				if sq_value == 0:
					for neighbor_div in sq_neighbors:
						if "blank" in neighbor_div["class"][1]:
							target_sq_id = neighbor_div["id"]
							to_click.append(target_sq_id)

					COMPLETED.append(rev_idify(div["id"]))
				
	if bool(to_click):
		print("Tactic 2")

		to_click = list(dict.fromkeys(to_click))
		for target_sq_id in to_click:
			target_sq = browser.find_element(By.ID, target_sq_id)
			if "blank" in target_sq.get_attribute("outerHTML"):
				target_sq.click()
				print("Clicking " + target_sq_id)
			
	numbered_sq.clear()

	# Randomizer

	if not (bool(to_flag) or bool(to_click)):
		print("Randomizer")

		random_sq_index = random.randint(0,479)
		random_sq_id = idify(random_sq_index)
		while "open" in browser.find_element(By.ID, random_sq_id).get_attribute("outerHTML"):
			random_sq_index = random.randint(0,479)
			random_sq_id = idify(random_sq_index)

		print("Trying " + random_sq_id)
		random_sq = browser.find_element(By.ID, random_sq_id)
		random_sq.click()

	to_flag.clear()
	to_click.clear()

	if COMPLETED:
		GRID = [i for i in GRID if i not in COMPLETED]
		COMPLETED.clear()

	alive = smile()
	if alive == 1:
		print("Making progress...")

	elif alive == 2:
		print("Great Success!")

	else:
		print("Unlucky :(")