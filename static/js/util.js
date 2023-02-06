function erf(x) {
    // constants
    var a1 =  0.254829592;
    var a2 = -0.284496736;
    var a3 =  1.421413741;
    var a4 = -1.453152027;
    var a5 =  1.061405429;
    var p  =  0.3275911;

    // Save the sign of x
    var sign = 1;
    if (x < 0) {
        sign = -1;
    }
    x = Math.abs(x);

    // A&S formula 7.1.26
    var t = 1.0/(1.0 + p*x);
    var y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*Math.exp(-x*x);

    return sign*y;
}

function getSuffix(n){
    var suffix = 'th'
    switch(n){
        case 1: 
            suffix = 'st'
            break
        case 2:
            suffix = 'nd'
            break
        case 3:
            suffix = 'rd'
            break
    }
    return suffix
}

function randomInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomizeGameResult(game){
    odds = parseInt(game.home_win_prob * 1000)
    rand = randomInteger(0,1000)

    if(odds >= rand){
        winner = game.home
        loser = game.away
    }
    else{
        winner = game.away
        loser = game.home
    }

    return {"winner": winner, "loser": loser}
}

function randomizeTourneyGameResult(firstTeamWinProb){
    odds = parseInt(firstTeamWinProb * 10)
    rand = randomInteger(0,1000)
    if(odds >= rand) return true
    return false
}

function sort_by_key(array, key){
    return array.sort(function(b, a){
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}