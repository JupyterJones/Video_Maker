var currentMatchIndex = -1;
var matches = [];

function findAndHighlight(str) {
    removeHighlights();

    var textarea = document.getElementById("text");
    if (!textarea) {
        alert("Textarea element not found.");
        return;
    }

    var text = textarea.value;
    var regex = new RegExp(str, 'gi');
    var match;

    while ((match = regex.exec(text)) !== null) {
        matches.push({ start: match.index, end: match.index + match[0].length, type: 'textarea' });
    }

    highlightTextareaMatches(text, matches, textarea);
    highlightPageMatches(str);
    
    if (matches.length === 0) {
        alert("String '" + str + "' not found.");
        return;
    }
}

function highlightTextareaMatches(text, matches, textarea) {
    matches.forEach(function(match) {
        if (match.type === 'textarea') {
            var prefix = text.substring(0, match.start);
            var highlighted = text.substring(match.start, match.end);
            var suffix = text.substring(match.end);

            text = prefix + '<span class="highlight">' + highlighted + '</span>' + suffix;
        }
    });

    textarea.value = text;
}

function highlightPageMatches(str) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var node;
    var regex = new RegExp(str, 'gi');
    var match;
    
    while ((node = walker.nextNode())) {
        while ((match = regex.exec(node.nodeValue)) !== null) {
            matches.push({ node: node, index: match.index, length: match[0].length, type: 'page' });

            var span = document.createElement('span');
            span.className = 'highlight';
            var start = node.splitText(match.index);
            var end = start.splitText(match[0].length);
            var highlight = start.cloneNode(true);
            span.appendChild(highlight);
            start.parentNode.replaceChild(span, start);
        }
    }
}

function removeHighlights() {
    var textarea = document.getElementById("text");
    if (textarea) {
        textarea.value = textarea.value.replace(/<span class="highlight">(.*?)<\/span>/g, "$1");
    }

    var highlights = document.querySelectorAll('.highlight');
    highlights.forEach(function(span) {
        var parent = span.parentNode;
        parent.replaceChild(span.firstChild, span);
        parent.normalize();
    });

    matches = [];
}

function moveToNextOccurrence() {
    var searchStr = document.getElementById("search_input").value;
    if (searchStr === "") {
        alert("Please enter a search string.");
        return;
    }

    findAndHighlight(searchStr);

    if (matches.length > 0) {
        currentMatchIndex = (currentMatchIndex + 1) % matches.length;
        var match = matches[currentMatchIndex];

        if (match.type === 'page') {
            var range = document.createRange();
            var sel = window.getSelection();
            range.setStart(match.node, match.index);
            range.setEnd(match.node, match.index + match.length);
            sel.removeAllRanges();
            sel.addRange(range);

            match.node.parentElement.scrollIntoView({ behavior: "smooth", block: "center" });
        }
    }
}
