
import pandas as pd
import numpy as np
from helpers.helpers import *
from datetime import datetime
from random import sample, shuffle

def run_mass_sims(games, teams, from_date, num_sims):

	start_time = datetime.now()

	# Object we'll push sims into
	sim_teams = {}

	# Set up the initial list of teams and what we're keeping track of for the sims
	list_teams = teams.values.tolist()
	for idx, team in enumerate(list_teams):
		sim_teams[team[0]] = {'wins': [], 'places':[], 'tourneys':[]}

	# Loop through each sim
	for n in range(num_sims):
		sim_games = games.copy()
		results = simulate_remaining_games(sim_games)
		tourney_results = simulate_tourney(results['team_names'], teams)
		for idx, team in enumerate(results['team_names']):
			sim_teams[team]['wins'].append(results['wins'][idx])
			sim_teams[team]['places'].append(idx + 1)
			sim_teams[team]['tourneys'].append(tourney_results[idx])

	# Get sim results
	wins_sims, places_sims, tourney_sims = format_sim_results(sim_teams)

	# Calculate number of byes
	places_sims = calculate_num_byes(places_sims)

	# Write sims to JSON
	create_sims_json(wins_sims, places_sims, tourney_sims, from_date)
	
	# End timer and print success message
	end_time = datetime.now()
	print('Duration: {}'.format(end_time - start_time))


def calculate_num_byes(places):
	for team in places:
		team['byes'] = sum(team['places'][:4])
	return places


def create_sims_json(wins_sims, places_sims, tourneys_sims, from_date):
	wins_df, places_df, tourneys_df = pd.DataFrame(wins_sims), pd.DataFrame(places_sims), pd.DataFrame(tourneys_sims)
	wins_df, places_df, tourneys_df = wins_df.to_json(orient='records'), places_df.to_json(orient='records'), tourneys_df.to_json(orient='records')
	
	wins_f = open('static/json/sims/wins/' + from_date + '.json', "w")
	places_f = open('static/json/sims/places/' + from_date + '.json', "w")
	tourneys_f = open('static/json/sims/tourneys/' + from_date + '.json', "w")

	wins_f.write('var wins_sims = ' + wins_df)
	places_f.write('var places_sims = ' + places_df)
	tourneys_f.write('var tourneys_sims = ' + tourneys_df)
	
	wins_f.close()
	places_f.close()
	tourneys_f.close()


def format_sim_results(sim_teams):

	wins_sims = []
	places_sims = []
	tourneys_sims = []
	
	for team, values in sim_teams.items():
		wins = np.array(values['wins'])
		places = np.array(values['places'])
		tourneys = np.array(values['tourneys'])
		win_totals, win_counts = np.unique(wins, return_counts=True)
		place_ranks, place_counts = np.unique(places, return_counts=True)
		tourney_ranks, tourney_counts = np.unique(tourneys, return_counts=True)

		wins_list = []
		for n in range(0,19):
			if n in win_totals:
				idx = np.where(win_totals == n)
				wins_list.append(win_counts[idx][0])
			else:
				wins_list.append(0)

		places_list = []
		for n in range(1,15):
			if n in place_ranks:
				idx = np.where(place_ranks == n)
				places_list.append(place_counts[idx][0])
			else:
				places_list.append(0)

		tourneys_list = []
		for n in range(0,6):
			if n in tourney_ranks:
				idx = np.where(tourney_ranks == n)
				tourneys_list.append(tourney_counts[idx][0])
			else:
				tourneys_list.append(0)

		wins_team, places_team, tourneys_team = {}, {}, {}
		wins_team['display_name'], places_team['display_name'], tourneys_team['display_name'] = team, team, team
		wins_team['wins'], places_team['places'], tourneys_team['tourneys'] = wins_list, places_list, tourneys_list

		wins_sims.append(wins_team)
		places_sims.append(places_team)
		tourneys_sims.append(tourneys_team)

	return wins_sims, places_sims, tourneys_sims


def simulate_remaining_games(games):
	
	# Possible replacement - quicker than setting rng as column but seems to get stuck with same results sometimes on loop
	#games.loc[(games['away_score'] == 0) & (np.random.randint(0,1000,1)[0] > games['home_win_prob'] * 1000), 'winner'] = games['away']

	# Put simulated of winners of future games into winner column and get value counts
	games.loc[games['away_score'] == 0, 'rng'] = np.random.randint(0,1000,len(games.loc[games['away_score'] == 0]))
	games.loc[games['away_score'] == 0, 'winner'] = games['home']
	games.loc[games['rng'] > games['home_win_prob'] * 1000, 'winner'] = games['away']
	winners = games.value_counts('winner')
	win_counts = winners.tolist()
	team_names = winners.keys().tolist()
	
	# Tiebreakers
	ties = [x[1] for x in list_duplicates(win_counts)]

	for tie in ties:

		tied_team_names = [team_names[d] for d in tie]
		tied_games = games.loc[ (games['away'].isin(tied_team_names)) & (games['home'].isin(tied_team_names)) ]

		#print(tied_games)
		tied_team_wins = []
		tied_team_games = []
		tied_team_pcts = []
		for team in tie:
			tied_team_wins.append(len(tied_games.loc[tied_games['winner'] == team_names[team]]))
			if len(tie) != 2:
				tied_team_games.append(len(tied_games.loc[(tied_games['away'] == team_names[team]) | (tied_games['home'] == team_names[team])]))
				tied_team_pcts.append(tied_team_wins[-1] / tied_team_games[-1])


		# Possibly randomize still tied since we're not going past head-to-head
		metric_list = tied_team_wins if len(tie) == 2 else tied_team_pcts
		still_tied = [x[1] for x in list_duplicates(metric_list)]
		if still_tied:
			for group in still_tied:
				new_group = sample(group, len(group))
				if group != new_group:
					if len(group) == 2:	
						tied_team_names[group[1]], tied_team_names[group[0]] = tied_team_names[group[0]], tied_team_names[group[1]]
					else:
						sorted_tied_team_names = []
						for n, tn in enumerate(tied_team_names):
							if n in group:
								idx = group.index(n)
								sorted_tied_team_names.append(tied_team_names[new_group[idx]])
							else:
								sorted_tied_team_names.append(tn)
						tied_team_names = sorted_tied_team_names


		# Update original list with solved/randomized ties
		reordered_tied_teams = [x for _,x in sorted(zip(metric_list, tied_team_names), reverse=True)]	
		team_names[tie[0] : tie[len(tie) -1] + 1] = reordered_tied_teams
	
	# Return Info
	return {'team_names': team_names, 'wins': win_counts}


def simulate_tourney(team_names, teams):

	round_out = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,]

	games = [ 
		[ [12,13,1,1], [11,14,2,1] ],
		[ [8,9,0,1], [5, False,1,1], [6, False,2,1], [7,10,3,1] ],
		[ [1, False,0,0], [4, False,0,1], [3, False,1,0], [2, False,1,1] ],
		[ [False, False,0,0], [False, False,0,1] ],
		[ [False, False, False ,False] ]
	]

	# Reorder the teams DF by seed order
	teams = teams.set_index('display_name')
	teams = teams.loc[team_names]

	for rnd_idx, rnd in enumerate(games):
		for game_idx, game in enumerate(rnd):

			first_team = teams.iloc[game[0]-1]
			second_team = teams.iloc[game[1]-1]

			rng = np.random.randint(0,1000)
			first_team_win_pct = calculate_tourney_win_probability([ first_team, second_team ])
			first_team_win = True if rng < first_team_win_pct * 1000 else False
			winner = game[0] if first_team_win else game[1]
			loser = game[1] if first_team_win else game[0]

			round_out[loser-1] = rnd_idx

			if rnd_idx != 4:
				games[rnd_idx + 1][game[2]][game[3]] = winner
			else:
				round_out[winner-1] = 5

	return round_out
			

















