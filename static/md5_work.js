// Globals
var encode = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
            'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', 
            '2', '3', '4', '5', '6', '7', '8', '9', '+', 
            '.'];
var job, result, check1, check2;

// Checks if has localStorage
var haslocalStorage = (function() {
	try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
        return true;
    } catch(e) {
        return false;
    }
}());

// Inner analysis loop
function dostuff()
{
    // In case it gets interrupted
    if (check2 == encode.length)
	{
	    if (check1 != encode.length)
	    {
	        check1++;
	        check2 = 0;
	    }
	}
    
    if (check1 == encode.length && check2 == encode.length)
        return;
    
	var return_val = "";
	for (third in encode)
	{
		for (fourth in encode)
		{
			return_val += hex_md5(job + encode[check1] + encode[check2] + encode[third] + encode[fourth]);
		}
	}
	console.log("Done with md5 of " + job + encode[check1] + encode[check2] + "__");
	result += hex_md5(return_val);
	check2++;
	
	if (check2 % 16 == 0)
	    checkpoint();
	
	if (check2 == encode.length)
	{
	    if (check1 != encode.length)
	    {
	        check1++;
	        check2 = 0;
	    }
	    else
	    {
	        // Send results
            if (check1 == encode.length && check2 == encode.length)
            {
        	    console.log("Done with job. Sending.");
            	result = hex_md5(result);
            	$.ajax({
            		url: "http://jp.rmenez.es/result",
            		type: 'POST',
            		data: {project: "md5", result: result},
            		success: function(data){
            			localStorage.removeItem('md5_job');
            			localStorage.removeItem('md5_result');
            			localStorage.removeItem('md5_check1');
            			localStorage.removeItem('md5_check2');
            		}
            	});
            }
	    }
	}
	
	return;
}

// Checkpoint
function checkpoint()
{
    localStorage.setItem('md5_check1', check1);
    localStorage.setItem('md5_check2', check2);
    localStorage.setItem('md5_result', result);
    $.ajax({
		url: "http://jp.rmenez.es/checkpoint",
		data: {project: "md5", checkpoint: check1/encode.length + check2/(encode.length*encode.length)},
		type: 'GET'
	});
	return;
}

// Analysis loop
function analysis()
{
    result = localStorage.getItem('md5_result');
	if (result == null)
	    check1 = check2 = 0;
	else
	{
	    check1 = localStorage.getItem('md5_check1');
    	check1 = check1 ? check1 : 0;
    	check2 = localStorage.getItem('md5_check2');
    	check2 = check2 ? check2 : 0;
    }
    
    if (check1 == 0 && check2 == 0)
        result = "";
    
    console.log("Ready");
    
	setInterval(dostuff, 1);
}

$(document).ready(function() {
    // Only if has localStorage
    if (haslocalStorage) {
    	// Gets data if doesn't have it
    	job = localStorage.getItem('md5_job');
    	if (job == null)
    	{
    		$.ajax({
    			url: "http://jp.rmenez.es/getjob",
    			type: 'POST',
    			data: {project: "md5"},
    			success: function(data){
    				localStorage.setItem('md5_job', data);
    				job = data;
    				console.log("Job set to " + data);
    				analysis();
    			}
    		});
    	}
    	else
    	    analysis();
    }
});