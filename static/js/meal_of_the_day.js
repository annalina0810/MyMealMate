document.addEventListener('DOMContentLoaded', function() {
    var meal_cookie = document.getElementsByClassName('meal_of_the_day')[0].getAttribute('meal_of_the_day');
    var meal = JSON.parse(meal_cookie.replaceAll("'","\"").replaceAll("None","null"));
    getIngredients(meal);
});

function getIngredients(meal) {

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