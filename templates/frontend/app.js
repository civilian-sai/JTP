$(document).ready(function() {
    // Handle form submission
    $('#recommendation-form').submit(function(event) {
        event.preventDefault();

        // Get form data
        var formData = {
            'calories': $('#calories').val(),
            'fat': $('#fat').val(),
            'saturated_fat': $('#saturated_fat').val(),
            'cholesterol': $('#cholesterol').val(),
            'sodium': $('#sodium').val(),
            'carbohydrate': $('#carbohydrate').val(),
            'fiber': $('#fiber').val(),
            'sugar': $('#sugar').val(),
            'protein': $('#protein').val(),
            'diet': $('input[name="diet"]:checked').val()
        };

        // Send POST request to backend
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/recommendation',
            data: formData,
            success: function(response) {
                displayRecommendations(response); // Display recommendations
            },
            error: function(xhr, status, error) {
                console.error('AJAX request failed:', error);
                handleError(xhr.responseJSON.error);
            }
        });
    });

    // Function to display recommendations
    function displayRecommendations(recipes) {
        var recommendationsContainer = $('#recommendations');
        recommendationsContainer.empty();

        // Define a default image URL for general dish photo
        var defaultImageUrl = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcOt2m-NOqLUy6nzH9fFoHiXXzntfJ23bVKQ&s';

        // Loop through each recipe and create cards
        for (var i = 0; i < recipes.length; i++) {
            var recipe = recipes[i];
            var recipeElement = $('<div class="col-md-6 mb-4"></div>'); // Create column for card

            // Create card element
            var card = $('<div class="card"></div>');

            // Create image element for the card
            var imgElement = $('<img class="card-img-top">');
            imgElement.attr('src', defaultImageUrl); // Set default image URL
            imgElement.appendTo(card);

            // Create card body
            var cardBody = $('<div class="card-body"></div>');

            // Add recipe name to card body
            var nameElement = $('<p class="card-title"><h3>Name:</h3> ' + recipe.Name + '</p>');
            var IngName= $('<p class="card-ingred"><h3>Ingredients:</h3>' +recipe.RecipeIngredientParts + '</p>')
            
            nameElement.appendTo(cardBody);
            IngName.appendTo(cardBody);

            // Add ingredients list to card body
    
            

            // Append card body to card
            cardBody.appendTo(card);

            // Append card to recipeElement
            card.appendTo(recipeElement);

            // Append recipeElement to recommendationsContainer
            recommendationsContainer.append(recipeElement);

            // Add clearfix div after every second card
         /*   if ((i + 1) % 2 === 0) {
                recommendationsContainer.append('<div class="w-100"></div>');
            }*/
        }
    }

    // Function to handle errors
    function handleError(errorMessage) {
        var errorContainer = $('<div class="error"></div>');
        errorContainer.text(errorMessage);
        $('body').prepend(errorContainer);

        // Remove the error message after 5 seconds
        setTimeout(function() {
            errorContainer.remove();
        }, 5000);
    }
});
