var currentMatchIndex = 0;
var matches = [];

function findAndHighlight(str) {
    // Remove previous highlights
    removeHighlights();

    // Find all text nodes and highlight matches
    var walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    var regex = new RegExp(str, 'gi');
    var node;
    while ((node = walker.nextNode())) {
        var match;
        while ((match = regex.exec(node.nodeValue)) !== null) {
            var span = document.createElement('span');
            span.className = 'highlight';
            var highlightedText = node.splitText(match.index);
            highlightedText.splitText(match[0].length);
            var highlightedNode = highlightedText.cloneNode(true);
            span.appendChild(highlightedNode);
            highlightedText.parentNode.replaceChild(span, highlightedText);
            matches.push(span);
        }
    }

    if (matches.length === 0) {
        alert("String '" + str + "' not found!");
        return;
    }

    // Reset currentMatchIndex after highlighting
    currentMatchIndex = 0;
}

function removeHighlights() {
    matches.forEach(function(span) {
        var parent = span.parentNode;
        parent.replaceChild(span.firstChild, span);
        parent.normalize();
    });
    matches = [];
}

function moveToNextOccurrence() {
    var searchStr = document.getElementById("search_input").value.trim();
    if (searchStr === "") {
        alert("Please enter a search string.");
        return;
    }

    if (matches.length === 0) {
        alert("No matches found for '" + searchStr + "'.");
        return;
    }

    // Move to next occurrence
    var currentMatch = matches[currentMatchIndex];
    currentMatch.scrollIntoView({ behavior: "smooth", block: "center" });
    currentMatchIndex = (currentMatchIndex + 1) % matches.length;
}
