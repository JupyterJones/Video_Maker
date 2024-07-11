function findAndHighlight(str) {
    removeHighlights();

    var textarea = document.getElementById("texts");
    if (!textarea) {
        alert("Textarea element not found.");
        return;
    }

    var text = textarea.value;
    var matches = [];
    var regex = new RegExp(str, 'gi');
    var match;

    while ((match = regex.exec(text)) !== null) {
        matches.push({ start: match.index, end: match.index + match[0].length });
    }

    if (matches.length === 0) {
        alert("String '" + str + "' not found in the textarea.");
        return;
    }

    matches.forEach(function(match) {
        var start = match.start;
        var end = match.end;
        
        var prefix = text.substring(0, start);
        var highlighted = text.substring(start, end);
        var suffix = text.substring(end);
        
        textarea.value = prefix + '<span class="highlight">' + highlighted + '</span>' + suffix;
    });
}

function removeHighlights() {
    var textarea = document.getElementById("text");
    if (textarea) {
        textarea.value = textarea.value.replace(/<span class="highlight">(.*?)<\/span>/g, "$1");
    }
}

// Rest of your script remains the same