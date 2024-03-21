// Global variables to keep track of selected month and year
var selected_month = new Date().getMonth();
var selected_year = new Date().getFullYear();

// Function to create the calendar
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

// Function to parse the schedule string into an object
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

// Function to handle form submission for meal scheduling
function scheduleMeal(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form data
    var form = event.target;
    var meal_name = form['meal-name'].value;
    var meal_date = form['meal-date'].value;

    // Send a POST request to the server to schedule the meal
    fetch('/schedule/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'meal-name=' + encodeURIComponent(meal_name) + '&meal-date=' + encodeURIComponent(meal_date),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to schedule meal');
        }
    })
    .then(data => {
        // Reload the page to update the calendar with the scheduled meal
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Update the calendar when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    var schedule = '{{ schedule }}';
    createCalendar(selected_month, selected_year, schedule);
    
    // Add event listener for form submission
    var form = document.getElementById('meal-scheduling-form');
    form.addEventListener('submit', scheduleMeal);
});

