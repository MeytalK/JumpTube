// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.



// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
	
	var action_url = "http://54.77.131.108";
//	var action_url = "http://127.0.0.1:8000";
	action_url += "/jump/?lang=en&from_youtube=" + tab.url;

	chrome.tabs.update(tab.id, { url: action_url });

});
