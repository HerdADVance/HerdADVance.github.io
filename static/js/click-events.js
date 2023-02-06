function initClickEvents(){
	
	// MAIN NAV LI CLICK
	$('nav li').click(function(){
		var current_wrap = '#' + $('nav li.active').attr('data-wrap') + '-table-wrap'
		var clicked_wrap = '#' + $(this).attr('data-wrap') + '-table-wrap'
		var current_id = $('nav li.active').attr('id')
		var clicked_id = $(this).attr('id')
		$('nav li').removeClass('active')
		$(this).addClass('active')

		if(current_wrap != clicked_wrap){
			$(current_wrap).animate({
				top: "-1500px"
			}, 200, function() {});

			$(clicked_wrap).animate({
				top: "0px"
			}, 200, function() {});
		}

		if(clicked_id == 'bracket'){
			moveToBracket()
		} else{
			removeConfetti()
		}

		if(clicked_id == 'schedule'){
			moveToSchedule()
		}

	})


	// SCHEDULE START/PAUSE SIM BUTTON
	$('#schedule-sim-control').click(function(){
		var isPlaying = parseInt($(this).attr('data-playing'))
		
		if(isPlaying){
			$(this).text("Continue Simulation")
			$(this).attr('data-playing', 0)
			clearSimulationInterval()

		} else{
			$(this).text("Pause Simulation")
			$(this).attr('data-playing', 1)
			startSimulationInterval()
		}

	})


	// BRACKET SIM ALL GAMES
	$('#bracket-sim-all').click(function(){
		startTourneyInterval()
	})

	// BRACKET SIM ONE GAME
	$('#bracket-sim-one').click(function(){
		simulateTourneyGame()
	})


}