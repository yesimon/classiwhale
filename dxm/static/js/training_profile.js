function setWhaleProgress(value, min, max)
{
    var newValue = Math.floor(100*(value - min)/(max - min));
    $(".whale-progress-bar").progressbar({
	value: newValue
    }); 
}