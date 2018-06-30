$(document).ready(function() {
	//code here...
	var code = $(".codetextarea")[0];
	var editor = CodeMirror.fromTextArea(code, {
		lineNumbers : true,
		matchBrackets: true,
    	mode: "text/x-c++src"
	});
});

$(document).ready(function() {
	//code here...
	var code = $(".codetextareaa")[0];
	var editor = CodeMirror.fromTextArea(code, {
		lineNumbers : true,
		matchBrackets: true,
    	mode: "text/x-c++src"
	});
});