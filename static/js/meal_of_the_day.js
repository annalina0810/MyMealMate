document.addEventListener('DOMContentLoaded', function() {
    var meal_cookie = document.getElementsByClassName('meal_of_the_day')[0].getAttribute('meal_of_the_day');
    var meal = JSON.parse(meal_cookie.replaceAll("'","\"").replaceAll("None","null"));
    meal = collectIngredients(meal);
    displayIngredients(meal)
});

function displayIngredients(meal) {
    var ingredients = ""
    for (var i=0; i<meal.ingredients.length;i++) {
        ingredients += "<li>"+meal.measurement_amounts[i]+" "+meal.measurement_units[i]+" "+meal.ingredients[i]+"</li>";
    }
    document.getElementById("ingredients").innerHTML = ingredients;
}

function collectIngredients(meal) {
    var ingredients = [];
    var measurement_amounts = [];
    var measurement_units = [];
    for (var i = 1; i <= 20; i++) {
        var ingredientKey = "strIngredient" + i;
        var measureKey = "strMeasure" + i;
        if (meal[ingredientKey] && meal[measureKey]) {
            ingredients.push(meal[ingredientKey]);
            var measurement = parseMeasurement(meal[measureKey]);
            measurement_amounts.push(measurement.amount);
            measurement_units.push(measurement.unit);
        }
    }

    return {
        idMeal: meal.idMeal,
        strMeal: meal.strMeal,
        strDrinkAlternate: meal.strDrinkAlternate,
        strCategory: meal.strCategory,
        strArea: meal.strArea,
        strInstructions: meal.strInstructions,
        strMealThumb: meal.strMealThumb,
        strTags: meal.strTags,
        strYoutube: meal.strYoutube,
        ingredients: ingredients,
        measurement_amounts: measurement_amounts,
        measurement_units: measurement_units,
        strSource: meal.strSource,
        strImageSource: meal.strImageSource,
        strCreativeCommonsConfirmed: meal.strCreativeCommonsConfirmed,
        dateModified: meal.dateModified
    };
}

function parseMeasurement(measurement) {
    var regex = /^(\d+(\.\d+)?)?\s*([^\d]+)?$/;
    var match = measurement.match(regex);
    var amount = 1;
    var unit = measurement.trim();
    if (match) {
        amount = match[1] ? parseFloat(match[1]) : 1;
        unit = match[3] !== undefined ? match[3].trim() : '';
    }
    return { amount: amount, unit: unit };
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