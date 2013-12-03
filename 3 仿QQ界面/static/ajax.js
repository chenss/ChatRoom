// 创建XMLHTTPRequest对象
function createXMLHttpRequest() {
	if(window.ActiveXObject){ 	// 判断是否支持ActiveX控件
		return new ActiveObject('Microsoft.XMLHTTP') 	// 通过实例化ActiveXObject的一个新实例来创建XMLHTTPRequest对象
	}
	else { 	// 判断是否把XMLHTTPRequest实现为一个本地javascript对象
		return new XMLHttpRequest() 	// 创建XMLHTTPRequest的一个实例（本地javascript对象）
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
