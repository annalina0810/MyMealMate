document.addEventListener('DOMContentLoaded', function() {
    var meal_cookie = getMealCookie('meal_cookie');
    var meal_cookie = document.getElementsByClassName('meal_of_the_day')[0].getAttribute('meal_of_the_day');
    var xmlhttp	= new XMLHttpRequest();	
    if (meal_cookie != null) {
        var url	= "https://www.themealdb.com/api/json/v1/1/search.php?s="+meal_cookie.replaceAll("\"", "");
    }
    xmlhttp.onreadystatechange = function() {	
        if (this.readyState == 4 && this.status == 200) {	
            var meal = JSON.parse(this.responseText).meals[0];
            displayMeal(meal);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
});

function getMealCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            mealStr = cookie.substring(name.length + 1);
            return mealStr;
        }
    }
    return null;
}

function displayMeal(meal) {
    var disp = "";
    disp += meal.strMeal + "<br>";
    disp += "<br><img class='thumbnail' src='"+meal.strMealThumb+"'>";
    document.getElementById("meal_of_the_day").innerHTML = disp;
}

function formatNewLines(str) {
    return str.replace(/\n/g, '<br>');
}

function getIngredients() {

}

// {"meals":[{
//     "idMeal":"",
//     "strMeal":"",
//     "strDrinkAlternate":,
//     "strCategory":"",
//     "strArea":"",
//     "strInstructions":"",
//     "strMealThumb":"",
//     "strTags":"",
//     "strYoutube":"",
//     "strIngredient1":"",
//     "strMeasure1":"",
//     "strSource":"",
//     "strImageSource":"",
//     "strCreativeCommonsConfirmed":"",
//     "dateModified":
// }]}