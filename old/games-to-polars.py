games = pl.from_pandas(games)

num_list = np.random.randint(0,1000,len(games))
games = games.with_column(pl.Series(name="rng", values=num_list))

games = games.with_columns([
		pl.when(col('winner').is_null()).then(
			pl.when(col('rng') > col('home_win_prob') * 1000 ).then(col('away')).otherwise(col('home')).alias('sim_winner')
		).otherwise(
			col('winner').alias('sim_winner')
		)
])

games = games.with_columns([
 		pl.when(col('sim_winner') != col('away') ).then(col('away')).otherwise(col('home')).alias('sim_loser')
])

games = games.groupby(['sim_winner']).agg(pl.count()).sort('count').reverse()