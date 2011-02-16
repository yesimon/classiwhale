var whaleExp;
var minExp;
var maxExp;

function setWhaleProgress(value, min, max)
{
    whaleExp = value;
    minExp = min;
    maxExp = max;
    var newValue = Math.floor(100*(value - min)/(max - min));
    $(".whale-progress-bar").progressbar({
	value: newValue
    }); 
}