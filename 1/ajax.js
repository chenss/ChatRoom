function createXMLHttpRequest() {
	if(window.XmlHttpRequest)
		return new XmlHttpRequest()
	else
		return new ActiveXobject("Microsoft.XMLHTTP")
	//alert('createXMLHttpRequest')
}

function ajax(type, url, data, fnSucc, fnFaild) {
	var request = createXMLHttpRequest()
	request.open(type, url, true)
	//alert('open XmlHttpRequest')
	if(type == "POST") {
		request.setRequestHeader('Content-Type',  'application/x-www-form-urlencoded')
		request.setRequestHeader("Content-length", data.length)
		request.setRequestHeader("Connection", "close")
	}
	request.send()
	//alert('send XmlHttpRequest')
	request.onreadystatechange = function() {
		if(request.readyState == 4) {
			if(request.status == 200) {
				fnSucc(request.responseText)
				//alert('responseText')
			}
			else {
				if(fnFaild)
					fnFaild(request.status)
			}
		}
	}
}