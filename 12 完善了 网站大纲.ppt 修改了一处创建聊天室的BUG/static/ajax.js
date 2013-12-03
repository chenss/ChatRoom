// 创建XMLHTTPRequest对象
function createXMLHttpRequest() {
	if(window.ActiveXObject){
		return new ActiveXObject("Msxml2.XMLHTTP")		//IE7及以上
	}
	else {
		return new XMLHttpRequest()		//firefox, chrome等
	}
}


function ajax(type, url, data, fnSucc, fnFaild) {
	var request = createXMLHttpRequest()
	request.open(type, url, true)
	if(type == 'POST') {
		request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	}
	request.send(data)
	request.onreadystatechange = function() {
		if(request.readyState == 4) {
			if(request.status == 200) {
				addChild(request.responseText)
			}
			else {
				if(fnFaild)
					fnFaild(request.status)
			}
		}
	}
}
