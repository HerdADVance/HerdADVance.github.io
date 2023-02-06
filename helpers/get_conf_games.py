
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

from helpers.helpers import *

def get_conf_games(teams):
	teams_scraped = []
	conf_games = []

	for idx, team in teams.iterrows():

		# Setting team_name variable just for easier usage later
		team_name = team.display_name

		# Keeping track of which teams already scraped to not include game duplicates
		teams_scraped.append(team_name)

		# Scrape Team page on ESPN
		response = requests.get(team['espn_url'], verify=False) # don't do this in prod

		# Parse the response with Beautiful Soup
		soup = BeautifulSoup(response.text, 'html.parser')

		# Loop through all team's games
		for scraped_game in soup.findAll("tr", {"class": "Table__TR"}):

			# Skip title/header rows in table
			skip_title = scraped_game.findAll("td", {"class": "Table__Title"})
			skip_headers = scraped_game.findAll("td", {"class": "Table_Headers"})
			if (len(skip_title) > 0) | (len(skip_headers) > 0):
				continue

			# Get all the game row's cells
			cells = scraped_game.findAll("td")

			# Get Opponent Name
			opponent_name_link = cells[1].findAll("span")[2].find("a")
			if opponent_name_link == None: # Team has no link and is not D-1 so also not conference game and we skip
				continue
			opponent_name = opponent_name_link.contents[0]

			# Find the conference opponent team
			team = teams.loc[teams['display_name'] == opponent_name]

			# Skip this game if not conference game or has already been scraped by previous team			
			if len(team) == 0:
				continue
			if team.iloc[0]['display_name'] in teams_scraped:
				continue

			# Set up game to be added to list of all conference gmes
			game = {}

			# Get Day and Location (home/away for this team)
			game['day'] = format_day(cells[0].find("span").contents[0])
			location = cells[1].find("span").contents[0]

			# Check if game is completed or hasn't played yet and add result/score if so
			result_cell_spans = cells[2].findAll("span")
			if len(result_cell_spans) > 1: # Completed
				result = result_cell_spans[0].contents[0]
				score = result_cell_spans[1].find("a").contents[0].split('-')
			else:
				result = False
			
			# Home and Away teams based on location
			if location == '@':
				game['away'] = team_name
				game['home'] = opponent_name
			else:
				game['away'] = opponent_name
				game['home'] = team_name

			# If result, add result and score
			game['winner'] = None
			if result:
				score[1] = score[1][:score[1].index(' ') + len(' ')].strip() # remove 'OT' from overtime scores
				if ( (location == '@' and result == 'W') | (location != '@' and result == 'L' ) ):
					game['away_score'] = int(score[0])
					game['home_score'] = int(score[1])
				else:
					game['away_score'] = int(score[1])
					game['home_score'] = int(score[0])
				if result == 'W':
					game['winner'] = team_name
				else:
					game['winner'] = opponent_name

			else:
				game['away_score'] = 0
				game['home_score'] = 0

			# Append game to list of all conference games
			conf_games.append(game)


	# Convert to DataFrame w/ correct col types
	conf_games = pd.DataFrame(conf_games)
	conf_games.home_score = conf_games.home_score.astype(int)
	conf_games.away_score = conf_games.away_score.astype(int)

	return conf_games

