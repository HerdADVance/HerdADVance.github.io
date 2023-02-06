import copy
import random

teams = [
	{"id": 0, "name": "Appalachian State", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 1, "name": "Coastal Carolina", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 2, "name": "Georgia Southern", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 3, "name": "Georgia State", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 4, "name": "James Madison", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 5, "name": "Marshall", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 6, "name": "Old Dominion", "division": "East", "wins": 0, "losses": 0, "division_wins": 0},
	
	{"id": 7, "name": "Arkansas State", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 8, "name": "Louisiana", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 9, "name": "South Alabama", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 10, "name": "Southern Miss", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 11, "name": "Texas State", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 12, "name": "Troy", "division": "West", "wins": 0, "losses": 0, "division_wins": 0},
	{"id": 13, "name": "UL Monroe", "division": "West", "wins": 0, "losses": 0, "division_wins": 0}
]

games = [

	# Games to be played
	[0, 5, 0],
	[0, 6, 0],
	[0, 2, 0],
	[1, 10, 0],
	[1, 4, 0],
	[2, 8, 0],
	[2, 5, 0],
	[3, 13, 0],
	[3, 4, 0],
	[3, 5, 0],
	[4, 6, 0],
	[6, 9, 0],
	[7, 11, 0],
	[7, 12, 0],
	[8, 11, 0],
	[9, 11, 0],
	[9, 10, 0],
	[10, 13, 0],
	[12, 13, 0],

	# Games already played
	[0, 12, 1],
	[4, 0, 1],
	[11, 0, 1],
	[0, 3, 1],
	[1, 0, 1],
	[1, 3, 1],
	[1, 2, 1],
	[1, 13, 1],
	[6, 1, 1],
	[1, 5, 1],
	[3, 2, 1],
	[2, 4, 1],
	[2, 6, 1],
	[9, 2, 1],
	[3, 6, 1],
	[3, 10, 1],
	[4, 11, 1],
	[4, 7, 1],
	[5, 4, 1],
	[12, 5, 1],
	[8, 5, 1],
	[5, 6, 1],
	[6, 7, 1],
	[7, 13, 1],
	[10, 7, 1],
	[8, 7, 1],
	[9, 7, 1],
	[13, 8, 1],
	[9, 8, 1],
	[10, 8, 1],
	[12, 8, 1],
	[9, 13, 1],
	[12, 9, 1],
	[12, 10, 1],
	[10, 11, 1],
	[12, 11, 1],
	[13, 11, 1],
]

# Create the East/West Champs dicts programatically
east_champs = {}
west_champs = {}
for i in range(7):
	east_champs[teams[i]['name']] = 0
	west_champs[teams[i+7]['name']] = 0

# Count wins and losses for games already played
for game in games:
	if game[2] == 1:
		winner = game[0]
		loser = game[1]
		teams[winner]['wins'] += 1
		teams[loser]['losses'] += 1
		if teams[winner]['division'] == teams[loser]['division']:
			teams[winner]['division_wins'] += 1


# Functions
def print_champs(east_champ, west_champ):
	print(east_champ + ' vs. ' + west_champ)


def get_champ(div):

	# Outright champion
	if div[0]['wins'] != div[1]['wins']:
		return div[0]['name']
	
	# Run Tiebreakers
	else:

		# Get list of all tied
		wins = div[0]['wins']
		tied_teams = list(filter(lambda div: div['wins'] == wins, div))

		# Loop through tied teams creating helpful lists for simplicity later
		tied_ids = []
		tied_wins = {}
		for team in tied_teams:
			tied_ids.append(team['id'])
			tied_wins[team['id']] = 0


		# Find all head-to-head games among tied teams
		tied_games = []
		for game in games:
			if game[0] in tied_ids and game[1] in tied_ids:
				tied_games.append(game)

		# Add win tallies in head-to-head games against tied teams
		for game in tied_games:
			winner = teams[game[0]]['id']
			tied_wins[winner] += 1

		# Sort those wins and convert dict to list
		tied_wins = dict(sorted(tied_wins.items(), key=lambda item: item[1], reverse=True))
		tied_wins = list(tied_wins.items())

		# Return winner if no longer tied
		if tied_wins[0][1] != tied_wins[1][1]:
			champ_id = tied_wins[0][0]
			return teams[champ_id]['name']

		# Eliminate those behind (if any) tied for 1st
		else:
			num_tied_before = len(tied_wins)
			wins = tied_wins[0][1]
			tied_wins = [x for x in tied_wins if x[1] == wins]
			num_tied_after = len(tied_wins)

		# Return to beginning of process if any team eliminated. Else continue to division wins
		if num_tied_before == num_tied_after:
			a = 'restart'
		else:

		# Sort remaining tied teams by division wins
			nonsense = True

		# Return winner if no longer tied

		# Eliminate those behind (if any) tied for 1st

		# Return to beginning of process if any team eliminated. Else continue to record against opposing division by standings


		# Return Champ Name
		print('\n')
		return div[0]['name']


def run_simulation(n):
	for i in range (n):
		sim_teams = copy.deepcopy(teams)
		for game in games:
			if game[2] == 0:
				if random.randrange(0,2) == 1:
					game[0], game[1] = game[1], game[0]

				winner = game[0]
				loser = game[1]
				sim_teams[winner]['wins'] += 1
				sim_teams[loser]['losses'] += 1
				if sim_teams[winner]['division'] == sim_teams[loser]['division']:
					sim_teams[winner]['division_wins'] += 1

		east = sorted(sim_teams[0:7], key=lambda d: d['wins'], reverse=True) 
		west = sorted(sim_teams[7:], key=lambda d: d['wins'], reverse=True)

		east_champ = get_champ(east)
		west_champ = get_champ(west)

		east_champs[east_champ] +=1
		west_champs[west_champ] +=1

		#print_champs(east_champ, west_champ)


# Start the sims
run_simulation(100)

# Print the sims
print(east_champs)
print(west_champs)











