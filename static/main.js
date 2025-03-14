// Function to fetch and display data
function fetchMealperiods(loc) {
    // Make an AJAX request to /mealperiods endpoint with appropriate parameters
    $.ajax({
        url: '/mealperiods',
        data: {
            location: loc
        },
        success: function (data) {
            // Update the content of the data-container div with the received data
            data.forEach(function (mealPeriod) {
                $('#mealperiods').append('<li><a class="dropdown-item" href="#">' + mealPeriod + '</a></li>');
            })
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });
}

function updateFoodItems(mealPeriod, data) {
    // Replace the content or update as needed
    $('#prompt').html('<h1>What did you eat?</h1>');

    // You can also add a new dropdown for food items or perform additional AJAX requests here
    $('#mealperiods-dropdown').addClass('d-none');
    data.sort(function(a, b) {
        return b.category.localeCompare(a.category);
    });
    data.forEach(function (foodItem) {
        var name = foodItem["name"];
        $('#fooditems').append('<label for="' + foodItem["name"] + '" class="form-label">' + name + '</label>'
                                    + '<div class="input-group mb-3">'
                                    + '<input type="number" name="' + name + '" step="any" min="0" max="50" aria-label="'
                                    + name + '" class="form-control" id="' + name + '" placeholder="Enter quantity - ' + foodItem["servingSize"] + '">'
                                    + '<input type="hidden" name="' + name + '" value="' + foodItem["calories"] + '">'
                                    + '<input type="hidden" name="' + name + '" value="' + foodItem["fat"] + '">'
                                    + '<input type="hidden" name="' + name + '" value="' + foodItem["carbs"] + '">'
                                    + '<input type="hidden" name="' + name + '" value="' + foodItem["protein"] + '">'
                                    + '<input type="hidden" name="' + name + '" value="' + foodItem["sugar"] + '">'
                                    + '</div>');
    })
}

function fetchFoodItems(mealperiod, loc) {
    // Make an AJAX request to /get_data endpoint with appropriate parameters
    $.ajax({
        url: '/get_data',
        data: {
            location: loc,
            mealperiod: mealperiod
        },
        success: function (data) {
            // Update the content of the data-container div with the received data
            return updateFoodItems(mealperiod, data);
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });
}

$(document).ready(function () {
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    let params = new URLSearchParams();
    let invalidNames = new Set();
    let validNames = new Set();
    for (let input of this.elements) {
        if (invalidNames.has(input.name)) continue;
        if (!validNames.has(input.name) && !invalidNames.has(input.name) && (input.value <= 0 || input.value === '')) {
            invalidNames.add(input.name);
            continue;
        }
        params.append(input.name, input.value);
        if (!validNames.has(input.name)) {
            validNames.add(input.name);
        }
    }
    

            // Use fetch to send a POST request
        fetch(this.action, {
            method: 'POST',
            body: params
        }).then(response => response.text())
          .then(html => {
              document.open();
              document.write(html);
              document.close();
          }).catch(error => console.log('Error:', error));
});
});
