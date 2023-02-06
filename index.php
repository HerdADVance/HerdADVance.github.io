<!DOCTYPE html>
<head>
	<title>Sun Belt CBB Simulator</title>
	<link rel="icon" type="image/x-icon" href="/static/img/favicon.png">
	<link rel="stylesheet" href="/static/css/style.css?v=20"></style>
	<link rel="stylesheet" href="/static/css/colors.css?v=4"></style>
	<link rel="stylesheet" href="/static/vendor/jquery-ui-1.13.2.css"></style>
	<script src="/static/vendor/jquery-3.6.js"></script>
	<script src="/static/vendor/jquery-ui-1.13.2.js"></script>
	<script src="/static/json/games.json"></script>
	<script src="/static/json/teams.json"></script>
	<script src="/static/json/sims/wins/02-05-23.json"></script>
	<script src="/static/json/sims/places/02-05-23.json"></script>
	<script src="/static/json/sims/tourneys/02-05-23.json"></script>
	<script src="/static/js/util.js"></script>
	<script src="/static/js/click-events.js"></script>
	<script src="/static/js/print.js"></script>
	<script src="/static/vendor/confetti.js"></script>
	<script src="/static/js/script.js"></script>
</head>
<body>
	
	<nav>
		<img src="/static/img/sbc-logo.png" class="conf-logo" alt="Sun Belt Conference logo">
		<h1>2022-23 Men's Basketball Odds</h1>
		<ul>
			<span>Simulate Season</span>
			<li id="schedule" data-wrap="standings" class="active">Schedule</li>
			<li id="bracket" data-wrap="standings">Bracket</li>
			<span>Results of 10,000 Sims</span>
			<li data-wrap="sims-wins">Win Totals</li>
			<li data-wrap="sims-places">Regular Season</li>
			<li data-wrap="sims-tourneys">Tournament</li>
		</ul>

	</nav>
	
	<div class="feature-wrap table-wrap" id="standings-table-wrap">
		<div id="schedule-wrap">
			<div class="standings-options">
				<button class="standings-controls" id="schedule-sim-control" data-started="0" data-playing="0">Sim Rest of Season</button>
				<div id="slider-wrap">
					<span class="slider-title">Sim Speed</span>
					<div id="slider"></div>
				</div>
			</div>
			<table class="table clear" id="standings-table">
				<thead></thead>
				<tbody></tbody>
			</table>
		</div>
		<div id="bracket-wrap">
			<div class="bracket-controls">
				<button class="standings-controls" id="bracket-sim-all" disabled>Sim Entire Tournament</button>
				<button class="standings-controls" id="bracket-sim-one" disabled>Sim Next Game</button>
			</div>
			<div class="bracket-round round-1">
				<div class="bracket-game" data-game="0">
					<div class="bracket-team" data-seed="12"></div>
					<div class="bracket-team" data-seed="13"></div>
				</div>
				<div class="bracket-game" data-game="1">
					<div class="bracket-team" data-seed="11"></div>
					<div class="bracket-team" data-seed="14"></div>
				</div>
			</div>
			<div class="bracket-round round-2">
				<div class="bracket-game" data-game="2">
					<div class="bracket-team" data-seed="8"></div>
					<div class="bracket-team" data-seed="9"></div>
				</div>
				<div class="bracket-game" data-game="3">
					<div class="bracket-team" data-seed="5"></div>
					<div class="bracket-team" data-advance-from="0"></div>
				</div>
				<div class="bracket-game" data-game="4">
					<div class="bracket-team" data-seed="6"></div>
					<div class="bracket-team" data-advance-from="1"></div>
				</div>
				<div class="bracket-game" data-game="5">
					<div class="bracket-team" data-seed="7"></div>
					<div class="bracket-team" data-seed="10"></div>
				</div>
			</div>
			<div class="bracket-round round-3">
				<div class="bracket-game" data-game="6">
					<div class="bracket-team" data-seed="1"></div>
					<div class="bracket-team" data-advance-from="2"></div>
				</div>
				<div class="bracket-game" data-game="7">
					<div class="bracket-team" data-seed="4"></div>
					<div class="bracket-team" data-advance-from="3"></div>
				</div>
				<div class="bracket-game" data-game="8">
					<div class="bracket-team" data-seed="3"></div>
					<div class="bracket-team" data-advance-from="4"></div>
				</div>
				<div class="bracket-game" data-game="9">
					<div class="bracket-team" data-seed="2"></div>
					<div class="bracket-team" data-advance-from="5"></div>
				</div>
			</div>
			<div class="bracket-round round-4">
				<div class="bracket-game" data-game="10">
					<div class="bracket-team" data-advance-from="6"></div>
					<div class="bracket-team" data-advance-from="7"></div>
				</div>
				<div class="bracket-game" data-game="11">
					<div class="bracket-team" data-advance-from="8"></div>
					<div class="bracket-team" data-advance-from="9"></div>
				</div>
			</div>
			<div class="bracket-round round-5">
				<div class="bracket-game" data-game="12">
					<div class="bracket-team" data-advance-from="10"></div>
					<div class="bracket-team" data-advance-from="11"></div>
				</div>
			</div>
			<div class="bracket-round round-champ">
				<div class="bracket-game">
					<div class="bracket-team" data-advance-from="12"></div>
				</div>
			</div>
			<div id="confetti-wrap"></div>
		</div>
	</div>

	<div class="feature-wrap table-wrap sims-table-wrap" id="sims-wins-table-wrap">
		<table class="table sims" id="sims-wins">
			<thead></thead>
			<tbody></tbody>
		</table>
	</div>

	<div class="feature-wrap table-wrap sims-table-wrap" id="sims-places-table-wrap">
		<!--h1>2022-23 SBC Regular Season Finish Odds</h1>
		<h2>Results of 10,000 sims based on win probabilities from KenPom AdjEM data</h2-->
		<table class="table sims" id="sims-places">
			<thead></thead>
			<tbody></tbody>
		</table>
	</div>

	<div class="feature-wrap table-wrap sims-table-wrap" id="sims-tourneys-table-wrap">
		<table class="table sims" id="sims-tourneys">
			<thead></thead>
			<tbody></tbody>
		</table>
	</div>

	

</body>
</html>