// logic for date
// default to creating a schedule for current month
// if the select previous or next month, use selected_month instead
// if the today button is clicked, use current month

// create calendar object structure
// get date
// get first day of month
// structure will be days of the week as heading, and then the days of the month
// so for if the first day of the month is a Wednesday, then the first 2 days of the month will be empty
// then the days of the month will be filled in, and then the last days of the month will be empty until the end of the wee

var selected_day = new Date().getDate();
var selected_month = new Date().getMonth();
var selected_year = new Date().getFullYear();

document.addEventListener('DOMContentLoaded', function() {
    createCalendar(selected_month, selected_year);
});

function createCalendar(month, year) {
    var days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var first_day = new Date(year, month, 1);
    var last_day = new Date(year, month + 1, 0);
    var calendar = "<table class='calendar'>";
    // alert("month: " + month + " year: " + year);
    calendar += "<caption>" + first_day.toLocaleString('default', { month: 'long' }) + " " + year + "</caption>";
    calendar += "<tr><th>" + days_of_week.join("</th><th>") + "</th></tr>";
    var day = 1;
    for (var i = 0; i < 6; i++) {
        calendar += "<tr>";
        for (var j = 0; j < 7; j++) {
            if (i == 0 && j < first_day.getDay()) {
                calendar += "<td></td>";
            } else if (day > last_day.getDate()) {
                break;
            } else {
                calendar += "<td><div id='scheduleDate'>" + day + "</div></td>";
                day++;
            }
        }
        calendar += "</tr>";
    }
    calendar += "</table>";
    document.getElementById("calendar").innerHTML = calendar;
}

function previousMonth() {
    selected_month -= 1;
    if (selected_month < 0) {
        selected_month = 11;
        selected_year -= 1;
    }
    createCalendar(selected_month, selected_year);
}

function nextMonth() {
    selected_month += 1;
    if (selected_month > 11) {
        selected_month = 0;
        selected_year += 1;
    }
    createCalendar(selected_month, selected_year);
}

function today() {
    selected_month = new Date().getMonth();
    createCalendar(selected_month, selected_year);
}


