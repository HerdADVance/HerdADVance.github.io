
// REGULAR SEASON STANDINGS TABLE
function printStandingsTableHeader(){
	var output = '<tr>'
		output += '<th colspan="2">'
		for(var i=0; i < games.length; i+=7){
			output += '<th>'
			// This would need to be changed for other conferences where all games aren't on the same dates
				var date = new Date(games[i].day + 21600000).toLocaleDateString("en-US").split('/') // adding 6 hours since date is GMT
				//var date = games[i].day.split('-')
				output += parseInt(date[0]) + '/' + parseInt(date[1])
			output +' </th'
		}
	output += '</tr>'
	$('#standings-table thead').html(output)
}

function printStandingsTable(){
	var output = ''
	for(var i=0; i < teams.length; i++){
		output += '<tr style="background-color:' + teams[i].primary_color + '; color:' + teams[i].secondary_color + ';">'
			output += '<td class="logo-name">'
				output += '<img src="/static/img/logos/' + teams[i].logo_filename + '.png"><span>' + teams[i].display_name + '</span>' 
			output += '</td>'
			//output += '<td class="name">' + teams[i].display_name + '</td>'
			output += '<td class="record">' + teams[i].wins + '-' + teams[i].losses + '</td>'
			for(var j=0; j < games.length; j++){
				if(games[j].away == teams[i].display_name || games[j].home == teams[i].display_name){

					var isHome = games[j].home == teams[i].display_name ? true : false
					var hasBeenPlayed = games[j].winner ? true : false
					var opponentName = isHome? games[j].away : games[j].home
					var winProb = isHome? games[j].home_win_prob : winProb = 1 - games[j].home_win_prob
					var opponentIndex = teams.findIndex(x => x.display_name === opponentName)
					var opponentLogo = teams[opponentIndex].logo_filename
					
					var result = ''
					if(hasBeenPlayed) result = games[j].winner == teams[i].display_name ? 'win' : 'loss'

					output += '<td class="game-box ' + result + '">'
						output += '<img src="/static/img/logos/' + opponentLogo  +'.png">'
						output += '<span class="win-prob">' + (winProb * 100).toFixed(1) + '%</span>'
						if(!isHome) output += '<span class="away">@</span>'
					output += '</td>'
				}
			}
		output += '</tr>'
	}

	$('#standings-table tbody').html(output)
}



// BRACKET AND BRACKET TEAMS/ODDS
function printStartingBracket(){
	for(var i=0; i < teams.length; i++){
		teams[i].tourney_seed = i+1 
		printBracketTeam(teams[i])
	}
}

function printBracketTeam(team){	
	var output = '<span class="bracket-seed">' + team.tourney_seed + '</span>'
	output += '<img src="/static/img/logos/' + team.logo_filename + '.png">'
	output += '<span class="bracket-name">' + team.display_name + '</span>'
	output += '<span class="bracket-odds"></span>'
	$('.bracket-team[data-seed=' + team.tourney_seed + ']').css('background-color', team.primary_color).css('color', team.secondary_color)
	$('.bracket-team[data-seed=' + team.tourney_seed + ']').html(output)
}

function printOpeningGamesOdds(){
	var gamesSet = [0,1,2,5]
	for(var i=0; i<gamesSet.length; i++){
		printTourneyGameOdds(gamesSet[i], false)
	}
}

function printTourneyGameOdds(gameId){
	var game = $('.bracket-game:eq(' + gameId + ')')
	var firstTeam = teams[teams.findIndex(x => x.display_name === $(game).find('.bracket-name:eq(0)').text())]
	var secondTeam = teams[teams.findIndex(x => x.display_name === $(game).find('.bracket-name:eq(1)').text())]

	// Calculate win probability
	var firstTeamExpPtDiff = ( firstTeam.adj_em - secondTeam.adj_em ) * ( firstTeam.adj_t + secondTeam.adj_t ) / 200
	var firstTeamWinProb = ((0.5 * (1 + erf((firstTeamExpPtDiff)/(11 * Math.sqrt(2)))) * 100).toFixed(1))
	var secondTeamWinProb = (100 - firstTeamWinProb).toFixed(1)

	// Display win probability
	$(game).find('.bracket-odds:eq(0)').text(firstTeamWinProb + '%')
	$(game).find('.bracket-odds:eq(1)').text(secondTeamWinProb + '%')
}



// SIMS WIN TOTALS TABLE
function printSimsWinsTableHeader(){
	var output = '<tr>'
		output += '<th colspan="2">'

		var maxWins = 18 - teams[0].losses
		var minWins = teams[teams.length-1].wins

		for(var i = maxWins; i > minWins - 1; i--){
			output += '<th>' + i + '-' + (18 - i) + '</th>'
		}
	output += '</tr>'
	$('#sims-wins thead').html(output)
}

function printSimsWinsTable(){
	var output = ''
	
	var maxWins = 18 - teams[0].losses
	var minWins = teams[teams.length-1].wins
	
	for(var i=0; i < teams.length; i++){
		simsIndex = wins_sims.findIndex(x => x.display_name === teams[i].display_name)
		simsTeam = wins_sims[simsIndex]
		var teamMaxWins = 18 - teams[i].losses
		var teamMinWins = teams[i].wins

		output += '<tr style="background-color:' + teams[i].primary_color + '; color:' + teams[i].secondary_color + ';">'
			output += '<td class="logo-name">'
				output += '<img src="/static/img/logos/' + teams[i].logo_filename + '.png"><span>' + teams[i].display_name + '</span>' 
			output += '</td>'
			output += '<td class="record">' + teams[i].wins + '-' + teams[i].losses + '</td>'
			for(var j = maxWins; j > minWins - 1; j--){
				var pct = (simsTeam.wins[j] / 100).toFixed(1)
				output += '<td class="sims-pct" data-pct="' + pct + '">'
					if(teamMaxWins < j || teamMinWins > j) output += '---'
				 	else output += pct + '%'
				output += '</td>'
				
			}
		output += '</tr>'
	}
	$('#sims-wins tbody').html(output)
}



// SIMS REGULAR SEASON PLACES TABLE
function printSimsPlacesTableHeader(){
	var output = '<tr>'
		output += '<th colspan="2">'
		for(var i=1; i < 15; i++){
			if(i == 5) output += '<th class="places-bye-header">Top 4</th>'
			var suffix = getSuffix(i)
			output += '<th>' + i + suffix + '</th>'
		}
	output += '</tr>'
	$('#sims-places thead').html(output)
}

function printSimsPlacesTable(){
	var output = ''
	for(var i=0; i < teams.length; i++){
		simsIndex = places_sims.findIndex(x => x.display_name === teams[i].display_name)
		simsTeam = places_sims[simsIndex]
		byePct = ( (simsTeam.places[0] + simsTeam.places[1] + simsTeam.places[2] + simsTeam.places[3]) / 100).toFixed(1)
		output += '<tr style="background-color:' + teams[i].primary_color + '; color:' + teams[i].secondary_color + ';">'
			output += '<td class="logo-name">'
				output += '<img src="/static/img/logos/' + teams[i].logo_filename + '.png"><span>' + teams[i].display_name + '</span>' 
			output += '</td>'
			output += '<td class="record">' + teams[i].wins + '-' + teams[i].losses + '</td>'
			for(var j=0; j < simsTeam.places.length; j++){
				if(j == 4) output += '<td class="places-bye-pct" data-places-bye-pct="' + byePct + '">' + byePct + '%</td>'
				var pct = (simsTeam.places[j] / 100).toFixed(1)
				output += '<td class="sims-pct" data-pct="' + pct + '">' + pct + '%</td>'
			}
		output += '</tr>'
	}
	$('#sims-places tbody').html(output)
}



// SIMS TOURNEY RESULTS TABLE
function printSimsTourneysTableHeader(){
	var output = '<tr>'
		output += '<th colspan="2">'

		var labels = ['R1 Loss', 'R2 Loss', 'QF Loss', 'SF Loss', 'CG Loss', 'Champion']

		for(var i = 0; i < 6; i++){
			output += '<th>' + labels[i] + '</th>'
		}
	output += '</tr>'
	$('#sims-tourneys thead').html(output)
}

function printSimsTourneysTable(){
	var output = ''
	for(var i=0; i < teams.length; i++){
		simsIndex = tourneys_sims.findIndex(x => x.display_name === teams[i].display_name)
		simsTeam = tourneys_sims[simsIndex]
		output += '<tr style="background-color:' + teams[i].primary_color + '; color:' + teams[i].secondary_color + ';">'
			output += '<td class="logo-name">'
				output += '<img src="/static/img/logos/' + teams[i].logo_filename + '.png"><span>' + teams[i].display_name + '</span>' 
			output += '</td>'
			output += '<td class="record">' + teams[i].wins + '-' + teams[i].losses + '</td>'
			for(var j=0; j < simsTeam.tourneys.length; j++){
				var pct = (simsTeam.tourneys[j] / 100).toFixed(1)
				output += '<td class="sims-pct" data-pct="' + pct + '">' + pct + '%</td>'
			}
		output += '</tr>'
	}
	$('#sims-tourneys tbody').html(output)
}






