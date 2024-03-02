var xmlhttp	= new XMLHttpRequest();	
var url	= "https://www.themealdb.com/api/json/v1/1/random.php";	
xmlhttp.onreadystatechange = function() {	
    if (this.readyState == 4 && this.status == 200) {	
        var meal = JSON.parse(this.responseText).meals[0];
        displayMeal(meal);
    }
};

xmlhttp.open("GET", url, true);
xmlhttp.send();

function displayMeal(meal) {
    document.getElementById("meal_of_the_day").innerHTML = meal.strMeal;	
}