
import random

num_sims = 100000
win_odds = [81.3,48.9,75.1,82.5,74.3,85.0,72.8,82.2,92.7,90.6,57.5,46.3,57.4,73.7,91.9,74.7,22.8,60.4]
win_outcomes = {}

for n in range(num_sims):

	wins = 0
	
	for odds in win_odds:
		odds = int(odds * 10)
		rand = random.randint(0,1000)
		if odds >= rand:
			wins += 1

	if wins in win_outcomes:
		win_outcomes[wins] += 1
	else:
		win_outcomes[wins] = 1

win_outcomes = reversed(sorted(win_outcomes.items()))

for wo in win_outcomes:
	print(str(wo[0]) + '-' + str(len(win_odds) - wo[0]) + ': ' + '{:.2%}'.format(wo[1] / num_sims) )

#print(sum(win_outcomes.values()))
