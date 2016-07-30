function Hide(target){
		document.getElementById(target).style.display= "none";
	}

	function Show(target){
		document.getElementById(target).style.display= "block";
	}
  function goBack() {
	window.history.back()
  }
  
  function getID(target) {
	var elemnt = document.getElementById(target);
	return elemnt;
  }
  

function loadURLAsynch(url, whereto, callback) {
	
	// Create an XMLHttpRequest object or ActiveX control
	if (window.XMLHttpRequest)  {
		var request = new XMLHttpRequest();
		var neednull = 1;
	}
	else if (window.ActiveXObject) {
		var request = new ActiveXObject("Microsoft.XMLHTTP");
		var neednull = 0;
	}
	
	// If XMLHTTPRequest is supported
	if (request) {
		// Set up asynchronous request
		try {
			request.open("GET", url, true);
		}
		catch (e) {
			alert("Error accessing server:\n"+e.toString());
		}

		request.onload = function(e) {
			if (request.readyState == 4)
				if (request.status == 200) {
            		var content = request.responseText;
					if (typeof(whereto) == 'object')
						whereto.innerHTML = content;
					if (callback)
						callback(content);
					return;
				}
			alert('Error ' + request.status + ' ' + request.responseText);
		}

		request.onerror = function(e) {
			alert('Error ' + request.status + ' ' + request.responseText);
		}

		// Send asynchronous request
		if (neednull) request.send(null)
		else request.send();
	}
}

function loadURLPostAsynch(url, data, whereto, callback) {
	
	// url may be a URI string or a form
	// If it is a form, it is sent using formdata and data is ignored
	// data may be a string or a dictionary
	if (window.XMLHttpRequest) 
		var request = new XMLHttpRequest();
	else if (window.ActiveXObject)
		var request = new ActiveXObject("Microsoft.XMLHTTP");
	
	// If XMLHTTPRequest is supported
	if (request) {
		// Set up asynchronous request
		var fd = null;
		if (typeof(url) == 'object' && url.nodeName == 'FORM') {
			var dest = url.action;
			fd = new FormData(url);
		}
		else
			var dest = url;

		try {
			request.open("POST", dest, true);
		}
		catch (e) {
			alert("Error accessing server:\n"+e.toString());
		}

		request.onload = function(e) {
			if (request.readyState == 4)
				if (request.status == 200) {
            		var content = request.responseText;
					if (typeof(whereto) == 'object')
						whereto.innerHTML = content;
					if (callback)
						callback(content);
					return;
				}
			alert('Error ' + request.status + ' ' + request.responseText);
		}

		request.onerror = function(e) {
			alert('Error ' + request.status + ' ' + request.responseText);
		}

		// Send asynchronous request
		if (fd)
			var senddata = fd;
		else if (typeof(data) == 'object') {
			var senddata = new FormData();
			for (var x in data) {
				senddata.append(x, data[x]);
			}
		}
		else {
			var senddata = data;
			request.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
		}

		request.send(senddata);
	}
}