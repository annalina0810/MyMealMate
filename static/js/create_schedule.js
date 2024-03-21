var selected_month = new Date().getMonth();
var selected_year = new Date().getFullYear();

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
    selected_year = new Date().getFullYear();
    createCalendar(selected_month, selected_year, schedule);
}

function scheduleMeal(event) {
    event.preventDefault();
    var form = event.target;
    var meal_name = form['meal-name'].value;
    var meal_date = form['meal-date'].value;
    var add_ingredients = form['add-ingredients'].checked; // check if the checkbox is checked

    var requestBody = 'meal-name=' + encodeURIComponent(meal_name) + '&meal-date=' + encodeURIComponent(meal_date);
    
    if (add_ingredients) {
        requestBody += '&add-ingredients=true'; // include parameter to add ingredients to shopping list
    }

    fetch('/MyMealMate/schedule/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: requestBody,
    })
    .then(response => {
        if (response.ok) {
            location.reload();
            return response.json();
        } else {
            throw new Error('Failed to schedule meal');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    var schedule = '{{ schedule }}';
    createCalendar(selected_month, selected_year, schedule);
    
    var form = document.getElementById('meal-scheduling-form');
    form.addEventListener('submit', scheduleMeal);
});
