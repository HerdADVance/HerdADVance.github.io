
import pandas as pd

from helpers.get_conf_games import *
from helpers.run_mass_sims import *
from helpers.helpers import *

# Options
conf = 'SB'
from_date = '02-05-23'
scrape_espn = True
mass_sim = True
saved_filepath = 'data/saved-scrapes/' + from_date + '.csv'

def get_games_and_teams():

	# Get conference teams from KenPom on certain date
	teams = get_teams_from_kenpom(conf, from_date)

	# Add ESPN URL and change display name for each team
	teams = add_teams_data(teams)

	# Scrape games and save locally or read already saved local file
	if scrape_espn:
		games = get_conf_games(teams)
		games.to_csv(saved_filepath)
	else:
		games = pd.read_csv(saved_filepath)

	# Add Win Probability to each game
	games = add_win_probability(games, teams)

	# Add wins and losses to teams in games that have already happened
	teams = count_wins_and_losses(games, teams)

	# Sort by relevant column
	teams = teams.sort_values(by='wins', ascending=False)
	games = games.sort_values(by='day', ascending=True)

	# Create JSON for front-end use
	create_json(teams, 'teams')
	create_json(games, 'games')

	# Simulate remaining games
	if mass_sim:
		mass_sim_results = run_mass_sims(games, teams, from_date, 10000)

	# Print Success message
	print("teams.json and games.json files created in static/json folder")

# Run Program
get_games_and_teams()


