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

function createCalendar(month, year, schedule) {

    schedule = parseSchedule(schedule);

    var days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var first_day = new Date(year, month, 1);
    var last_day = new Date(year, month + 1, 0);
    var calendar = "<table class='calendar'>";
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
                var date = year + "-" + (month + 1).toString().padStart(2, '0') + "-" + day.toString().padStart(2, '0');
                var meals = schedule[date];
                var meal_list = "";
                if (meals) {
                    meal_list = "<ul>";
                    meals.forEach(meal => {
                        meal_list += "<li>" + meal + "</li>";
                    });
                    meal_list += "</ul>";
                }
                calendar += "<td>" + day + "<br>" + meal_list + "</td>";
                day++;
            }
        }
        calendar += "</tr>";
    }
    calendar += "</table>";
    document.getElementById("calendar").innerHTML = calendar;
}

function parseSchedule(schedule) {
    var schedule_obj = {};
    var schedule_list = schedule.split(';');
    schedule_list.pop();
    schedule_list.forEach(day => {
        var day_list = day.split(',');
        var date = day_list.shift();
        schedule_obj[date] = day_list;
    });

    return schedule_obj;
}


function previousMonth(schedule) {
    selected_month -= 1;
    if (selected_month < 0) {
        selected_month = 11;
        selected_year -= 1;
    }
    createCalendar(selected_month, selected_year, schedule);
}

function nextMonth(schedule) {
    selected_month += 1;
    if (selected_month > 11) {
        selected_month = 0;
        selected_year += 1;
    }
    createCalendar(selected_month, selected_year, schedule);
}

function today(schedule) {
    selected_month = new Date().getMonth();
    createCalendar(selected_month, selected_year, schedule);
}


