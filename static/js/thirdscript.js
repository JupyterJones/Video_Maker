function findString(str) {
    var textarea = document.getElementById("text");
    var textareaValue = textarea.value;
    var strFound = false;

    if (!textarea) {
        alert("Textarea element not found.");
        return;
    }

    // Remove previous highlights
    removeHighlights();

    var startPos = 0;
    var index = textareaValue.indexOf(str, startPos);
    while (index !== -1) {
        var range = document.createRange();
        range.setStart(textarea, index);
        range.setEnd(textarea, index + str.length);

        var span = document.createElement("span");
        span.style.backgroundColor = "yellow";
        span.className = "highlight";
        range.surroundContents(span);

        strFound = true;

        startPos = index + str.length;
        index = textareaValue.indexOf(str, startPos);
    }

    if (!strFound) {
        alert("String '" + str + "' not found!");
    }
}

function removeHighlights() {
    var highlights = document.querySelectorAll('.highlight');
    highlights.forEach(function(span) {
        var parent = span.parentNode;
        parent.replaceChild(span.firstChild, span);
        parent.normalize();
    });
}

function moveToNextOccurrence() {
    var searchStr = document.getElementById("search_input").value.trim();
    if (searchStr === "") {
        alert("Please enter a search string.");
        return;
    }

    findString(searchStr);
}
