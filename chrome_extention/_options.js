// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.



function SelectLang() {
  if (window.localStorage == null) {
    alert('Local storage is required for changing providers');
    return;
  }  
    window.localStorage.Language = Lang;
	//window.alert(window.localStorage.Language);
  
}



document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#LangSelect').addEventListener('select', SelectLang);
});
