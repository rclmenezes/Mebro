var encode = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
            'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', 
            '2', '3', '4', '5', '6', '7', '8', '9', ',', 
            '.'];
var base = "{{ base }}";
var refresh = true; // Makes sure you have new base
console.log("Ready. Base is " + base);

var beforeSum = 0;
var afterSum = 0;
var total = 0;

function dostuff()
{
    var start = (new Date).getTime();
	var return_val = "";
	if (refresh == false)
		return;
	refresh = false;
	for (first in encode)
	{
		for (second in encode)
		{
			return_val += base + encode[first] + encode[second] + " " + hex_sha256(base + encode[first] + encode[second] + " ");
			//document.write(encode[first] + encode[second] + "<br/>");
		}
	}

	console.log("Finished hashing all combinations of " + base + "__");
	var diff = (new Date).getTime() - start;
	beforeSum += diff;
    //console.log("Before request: " + diff.toString());
	
	var url = 'http://jp.rmenez.es/ajax?base='+base+"&hashes="+return_val+"&jsoncallback=?";
	$.ajax({
		url: url,
		dataType: 'jsonp',
		jsonpCallback: 'callback123',
		success: function(data){
		    var diff = (new Date).getTime() - start;
		    afterSum += diff;
		    //console.log("After request: " + diff.toString());
			base = data.base;
			refresh = true;
			console.log("New base is  " + base);
		}
	});
	total += 1;
	console.log("Before sum: " + beforeSum/total.toString() + "After sum: " + afterSum/total.toString());
}
setInterval(dostuff,1000);
