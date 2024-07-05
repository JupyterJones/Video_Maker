
function findString(str) {
    if (parseInt(navigator.appVersion) < 4) return;

    if (window.find) {
        var strFound = window.find(str);
        if (!strFound) {
            window.find(str, 0, 1);
        }
        if (strFound) {
            var range = window.getSelection().getRangeAt(0);
            var span = document.createElement("span");
            span.style.backgroundColor = "yellow";
            range.surroundContents(span);
        }
    } else if (navigator.appName.indexOf("Microsoft") != -1) {
        // Not implemented for brevity
    } else if (navigator.appName == "Opera") {
        alert("Opera browsers not supported, sorry...");
        return;
    }

    if (!strFound) alert("String '" + str + "' not found!");
}

function moveToNextOccurrence() {
    var search_str = document.getElementById("search_input").value;
    findString(search_str);
}