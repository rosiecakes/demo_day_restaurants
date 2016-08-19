$(document).ready(function() { 
    // add parser through the tablesorter addParser method 
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'price_level', 
        is: function(s) { 
            // return false so this parser is not auto detected 
            return false; 
        }, 
        format: function(s) { 
            // format your data for normalization 
            return s.toLowerCase()
            .replace(/\$\$\$\$/,3)
            .replace(/\$\$\$/,2)
            .replace(/\$\$/,1)
            .replace(/\$/,0); 
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    }); 
    // call the tablesorter plugin 
    $("table").tablesorter({ 
        sortInitialOrder: "asc",
        sortList: [[0,0]],
        headers: { 
            6: { 
                sorter:'price_level' 
            } 
        } 
    });              
}); 