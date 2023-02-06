
# Imports
import pandas as pd
import polars as pl
from polars import col
import numpy as np
import math
from datetime import datetime
from collections import defaultdict


# Set up info for each team
def add_teams_data(teams):
	teams['wins'] = 0
	teams['losses'] = 0
	teams['tourney_seed'] = None
	teams['espn_url'] = teams['display_name'].apply(get_team_info_from_seeder, args=['espn_url'])
	teams['espn_name'] = teams['display_name'].apply(get_team_info_from_seeder, args=['espn_name'])
	teams['primary_color'] = teams['display_name'].apply(get_team_info_from_seeder, args=['primary_color'])
	teams['secondary_color'] = teams['display_name'].apply(get_team_info_from_seeder, args=['secondary_color'])
	teams['logo_filename'] = teams['display_name'].apply(get_logo_filename)
	teams['display_name'] = teams['display_name'].apply(get_team_info_from_seeder, args=['display_name']) # must be last in this func

	return teams


def add_win_probability(games, teams):
	games['home_win_prob'] = games.apply(calculate_win_probability, args=[teams], axis=1)
	games.home_win_prob = games.home_win_prob.astype(float)
	return games

def calculate_tourney_win_probability(teams):
	home = teams[0]
	away = teams[1]

	home_exp_pt_diff = ( home.adj_em - away.adj_em ) * ( home.adj_t + away.adj_t ) / 200 # no 3.75 adjustment for homecourt
	return 0.5 * (1 + math.erf((home_exp_pt_diff)/(11 * math.sqrt(2))))

def calculate_win_probability(game, teams, neutral=False):
	home = teams.loc[teams['display_name'] == game['home']].iloc[0]
	away = teams.loc[teams['display_name'] == game['away']].iloc[0]

	home_exp_pt_diff = ( home.adj_em - away.adj_em ) * ( home.adj_t + away.adj_t ) / 200 + 3.75
	return 0.5 * (1 + math.erf((home_exp_pt_diff)/(11 * math.sqrt(2))))

def create_json(df, df_name):	
	df = df.to_json(orient='records')
	f = open('static/json/' + df_name + '.json', "w")
	f.write('var ' + df_name + ' = ' + df)
	f.close()


def count_wins_and_losses(games, teams):
	completed_games = games.loc[games['away_score'] > 0]
	for idx, game in completed_games.iterrows():
		if game.away_score > game.home_score:
			winner = find_team_index_by_display_name(game.away, teams)
			loser = find_team_index_by_display_name(game.home, teams)
		else:
			winner = find_team_index_by_display_name(game.home, teams)
			loser = find_team_index_by_display_name(game.away, teams)

		teams.at[winner,'wins'] = teams.at[winner,'wins'] + 1 
		teams.at[loser,'losses'] = teams.at[loser,'losses'] + 1 

	return teams


def find_team_index_by_display_name(display_name, teams):
	team_index = teams[teams['display_name'] == display_name].index.item()
	return team_index

def format_day(day):
	dt = datetime.strptime(day, '%a, %b %d')
	if dt.month > 6:
		year = 2022
	else:
		year = 2023
	
	return dt.replace(year=year)

# Column names to match up with KenPom CSV data
def get_kenpom_column_names():
	col_names = [
		'ranked', 
		'display_name',
		'conf',
		'record',
		'adj_em',
		'adj_o',
		'adj_o_rank',
		'adj_d',
		'adj_d_rank',
		'adj_t',
		'adj_t_rank',
		'luck',
		'luck_rank',
		'sos_adj_em',
		'sos_adj_em_rank',
		'sos_adj_o',
		'sos_adj_o_rank',
		'sos_adj_d',
		'sos_adj_d_rank',
		'ooc_adj_em',
		'ooc_adj_em_rank',
	]

	return col_names


def get_logo_filename(team_name):
	return team_name.lower().replace(" ", "-").replace(".", "")


# Fetch the teams from KenPom based on conference and date
def get_teams_from_kenpom(conf, from_date):

	col_names = get_kenpom_column_names()
	kenpom_teams = pd.read_csv('data/kenpom/' + from_date + '.csv', names=col_names)
	kenpom_teams['ranked'] = pd.to_numeric(kenpom_teams['ranked'], errors = 'coerce')
	#kenpom_teams.dropna(inplace = True)
	kenpom_teams = kenpom_teams.dropna()
	kenpom_teams = kenpom_teams[kenpom_teams.conf == conf].copy(deep=False) # copy to prevent DataFrame slice SettingWithCopyWarning
	kenpom_teams = kenpom_teams[['display_name', 'adj_em', 'adj_t']]
	kenpom_teams.adj_em = kenpom_teams.adj_em.astype(float)
	kenpom_teams.adj_t = kenpom_teams.adj_t.astype(float)

	return kenpom_teams


# Team Seeder, uses KenPom name as key, collects display_name or espn_url
def get_team_info_from_seeder(team_name, column):

	team_seeds = {}

	# Sun Belt
	team_seeds['Appalachian St.'] = {"primary_color": "#1c1c1c", "secondary_color": "#fecd00", "display_name": "Appalachian State", "espn_name": "Appalachian St", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2026"}
	team_seeds['Coastal Carolina'] = {"primary_color": "#006f71", "secondary_color": "#c5a576", "display_name": "Coastal Carolina", "espn_name": "Coast Car", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/324"} 
	team_seeds['Georgia Southern'] = {"primary_color": "#001840", "secondary_color": "#ab9360", "display_name": "Georgia Southern", "espn_name": "Georgia So", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/290"} 
	team_seeds['Georgia St.'] = {"primary_color": "#3939c1", "secondary_color": "#FFF", "display_name": "Georgia State", "espn_name": "Georgia St", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2247"} 
	team_seeds['James Madison'] = {"primary_color": "#4e017d", "secondary_color": "#b4a76c", "display_name": "James Madison", "espn_name": "James Madison", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/256"} 
	team_seeds['Marshall'] = {"primary_color": "#00984d", "secondary_color": "#FFF", "display_name": "Marshall", "espn_name": "Marshall", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/276"} 
	team_seeds['Old Dominion'] = {"primary_color": "#002f59", "secondary_color": "#a2d2f1", "display_name": "Old Dominion", "espn_name": "Old Dominion", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/295"} 
	team_seeds['Arkansas St.'] = {"primary_color": "#d02030", "secondary_color": "#000", "display_name": "Arkansas State", "espn_name": "Arkansas St", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2032"} 
	team_seeds['Louisiana'] = {"primary_color": "#d2142a", "secondary_color": "#FFF", "display_name": "Louisiana", "espn_name": "Louisiana", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/309"} 
	team_seeds['South Alabama'] = {"primary_color": "#00205b", "secondary_color": "#bf133e", "display_name": "South Alabama", "espn_name": "South Alabama", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/6"} 
	team_seeds['Southern Miss'] = {"primary_color": "#ffd045", "secondary_color": "#000", "display_name": "Southern Miss", "espn_name": "Southern Miss", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2572"} 
	team_seeds['Texas St.'] = {"primary_color": "#571c1f", "secondary_color": "#ac9156", "display_name": "Texas State", "espn_name": "Texas St", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/326"}
	team_seeds['Troy'] = {"primary_color": "#afb0b3", "secondary_color": "#5e0410", "display_name": "Troy", "espn_name": "Troy", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2653"} 
	team_seeds['Louisiana Monroe'] = {"primary_color": "#FDBA0C", "secondary_color": "#6f082a", "display_name": "UL Monroe", "espn_name": "UL Monroe", "espn_url": "https://www.espn.com/mens-college-basketball/team/schedule/_/id/2433"}

	return team_seeds[team_name][column]


# Get indeces of duplicates from list
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)






