var gamesIterator = getStartingIterator();
var tourneyIterator = 0
var numGames = games.length
var numTourneyGames

var simulationInterval
var tourneyInterval
var simulationSpeed = 525
var tourneySpeed = 500
var tourneyDelay = 2000

$(document).ready(function() {

	// Print Tables
	printStandingsTableHeader()
	printSimsPlacesTableHeader()
	printSimsTourneysTableHeader()
	printSimsWinsTableHeader()
	printStandingsTable()
	printSimsPlacesTable()
	printSimsTourneysTable()
	printSimsWinsTable()

	// Standings Options and Slider
	initSlider()
	matchStandingsOptionsWidth()

	// Click Events
	initClickEvents()
	
});


function clearSimulationInterval(){
	clearInterval(simulationInterval)
}
function startSimulationInterval(){
	simulationInterval = setInterval(simulateGame, simulationSpeed);
}

function clearTourneyInterval(){
	clearInterval(tourneyInterval)
}
function startTourneyInterval(){
	tourneyInterval = setInterval(simulateTourneyGame, tourneySpeed);
}


function getStartingIterator(){
	for(var i=0; i < games.length; i++){
		if(games[i].away_score == 0){
			return i
		}
	}
}

function initSlider(){
	$(function(){
		$("#slider").slider({
			range: "min",
			value: 525,
			min: 50,
			max: 1000,
			slide: function(event, ui){
				simulationSpeed = 1050 - ui.value
				var isPlaying = parseInt($('#schedule-sim-control').attr('data-playing'))
				if (isPlaying){
					clearSimulationInterval()
					startSimulationInterval()
				}
			}
		});
	});
}

function toggleSimButtonsClickability(){
	$('#schedule-sim-control').attr('disabled', true)
	$('.bracket-controls button').attr('disabled', false)
}

function disableBracketSimButtons(){
	$('.bracket-controls button').attr('disabled', true)
}

function matchStandingsOptionsWidth(){
	var width = $('#standings-table').width()
	$('.standings-options').css('width', width)
}

function moveToBracket(){
	$('#schedule-wrap').animate({
		left: "-150%",
	}, 100, function() {});

	$('#bracket-wrap').animate({
		left: "190px",
		top: '0px'
	}, 100, function() {});

	if(!$('nav li#bracket').hasClass('active')){
		$('nav li').removeClass('active')
		$('nav li#bracket').addClass('active')
	}
}

function moveToSchedule(){
	$('#bracket-wrap').animate({
		left: '150%',
	}, 100, function() {});

	$('#schedule-wrap').animate({
		left: "0px"
	}, 100, function() {});

	if(!$('nav li#schedule').hasClass('active')){
		$('nav li').removeClass('active')
		$('nav li#schedule').addClass('active')
	}
}

function prepareTourney(){
	printStartingBracket()
	printOpeningGamesOdds()
	toggleSimButtonsClickability()
	numTourneyGames = $('.bracket-game').length
	setTimeout(moveToBracket, tourneyDelay)
}

function simulateTourneyGame(){

	if(tourneyIterator == numTourneyGames - 1){
		clearTourneyInterval()
		return
	}

	gameId = tourneyIterator
	
	var game = $('.bracket-game:eq(' + gameId + ')')
	var firstTeam = teams[teams.findIndex(x => x.display_name === $(game).find('.bracket-name:eq(0)').text())]
	var secondTeam = teams[teams.findIndex(x => x.display_name === $(game).find('.bracket-name:eq(1)').text())]

	// Simulate winner (returns true or false)
	var firstTeamWinProb = $(game).find('.bracket-odds:eq(0)').text().slice(0, -1); 
	firstTeamWon = randomizeTourneyGameResult(firstTeamWinProb)
	var winner = firstTeamWon? firstTeam : secondTeam

	// Advance winner to next round
	var output = '<span class="bracket-seed">' + winner.tourney_seed + '</span>'
	output += '<img src="/static/img/logos/' + winner.logo_filename + '.png">'
	output += '<span class="bracket-name">' + winner.display_name + '</span>'
	output += '<span class="bracket-odds"></span>'
	$('.bracket-team[data-advance-from=' + gameId + ']').html(output).css('background-color', winner.primary_color).css('color', winner.secondary_color)

	// Print Odds for game winner advanced to
	var nextGame = $('.bracket-team[data-advance-from=' + gameId + ']').parent()
	var nextGameId = nextGame.attr('data-game')
	if( nextGame.find('.bracket-name:eq(0)').text() != '' && nextGame.find('.bracket-name:eq(1)').text() != ''){
		printTourneyGameOdds(nextGameId)
	}

	// Advance iterator
	tourneyIterator ++

	// Tourney Over
	if(tourneyIterator == numTourneyGames - 1){
		disableBracketSimButtons()
		winnerColors = [winner.primary_color, winner.secondary_color]
		startConfetti()
		$('#confetti-canvas').appendTo('#confetti-wrap')
	}
}

function simulateGame(){
	if(gamesIterator == numGames){
		clearSimulationInterval()
		prepareTourney()
		return
	}

	simulatedResults = randomizeGameResult(games[gamesIterator])

	winnerIndex = teams.findIndex(x => x.display_name === simulatedResults.winner);
	loserIndex = teams.findIndex(x => x.display_name === simulatedResults.loser);

	teams[winnerIndex].wins += 1
	teams[loserIndex].losses += 1

	teams = sort_by_key(teams, 'wins')

	games[gamesIterator].winner = simulatedResults.winner

	gamesIterator ++

	printStandingsTable()
}


