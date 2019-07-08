// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


function getParameterByName(name, url) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
	//window.alert(tab.url);
//	var action_url = "http://127.0.0.1:8000/jump/?lang=iw&from_youtube=" + tab.url;
	var action_url = "http://127.0.0.1:8000/jump/?lang=iw&from_youtube=" + tab.url;
	chrome.tabs.update(tab.id, { url: action_url });
	
	
	
	
	/* var xhr = new XMLHttpRequest();
        var url = "http://127.0.0.1:8000/jump/?lang=en&from_youtube=" + tab.url;
	//tab.url = "http://127.0.0.1:8000/jump/?lang=iw&from_youtube=" + tab.url;
	//location.href  =  "http://127.0.0.1:8000/jump/?lang=iw&from_youtube=" + tab.url;
	xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                location.href  = url;			
				window.alert(tab.url);				
                }
            }
 */    
	//xhr.open('GET', url, true);
      //  xhr.send();
});
