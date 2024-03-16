document.addEventListener('DOMContentLoaded', function() {
    var meal_cookie = document.getElementsByClassName('meal_of_the_day')[0].getAttribute('meal_of_the_day');
    var meal = JSON.parse(meal_cookie.replaceAll("'","\"").replaceAll("None","null"));
    // meal = collectIngredients(meal);
    displayIngredients(meal);
});

function displayIngredients(meal) {
    var ingredients = ""
    meal["ingredients"].forEach(i => {
        ingredients += "<li>"+i["amount"]+" "+i["unit"]+" "+i["name"]+"</li>";
    });
    document.getElementById("ingredients").innerHTML = ingredients;
}

function displayAddButton(has_meal_of_the_day) {
    var form = document.getElementsByClassName('add_meal_of_the_day')[0];
    if (has_meal_of_the_day == "True") {
        form.style.display = 'none';
    }
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
//     "ingredients":{"name":"","amount":"","unit":""},
//     "strMeasure1":"",
//     "strSource":"",
//     "strImageSource":"",
//     "strCreativeCommonsConfirmed":"",
//     "dateModified":
// }]}