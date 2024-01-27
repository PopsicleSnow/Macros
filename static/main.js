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
    // For simplicity, let's assume a predefined list of food items
    $('#mealperiods-dropdown').addClass('d-none');
    data.forEach(function (foodItem) {
        $('#fooditems').append('<label for="' + foodItem[2] + '" class="form-label">' + foodItem[2] + '</label>'
                                    + '<div class="input-group mb-3"><span class="input-group-text">' + foodItem[8] + '</span>'
                                    + '<input type="number" name="' + foodItem[2] + '" min="0" value="0" aria-label="'
                                    + foodItem[2] + '" class="form-control" id="' + foodItem[2] + '" placeholder="0">'
                                    + '<input type="hidden" name="' + foodItem[2] + '" value="' + foodItem[3] + '">'
                                    + '<input type="hidden" name="' + foodItem[2] + '" value="' + foodItem[4] + '">'
                                    + '<input type="hidden" name="' + foodItem[2] + '" value="' + foodItem[5] + '">'
                                    + '<input type="hidden" name="' + foodItem[2] + '" value="' + foodItem[6] + '">'
                                    + '<input type="hidden" name="' + foodItem[2] + '" value="' + foodItem[7] + '">'
                                    + '</div>');
    })
}

function fetchFoodItems(mealperiod, loc) {
    // Make an AJAX request to /fooditems endpoint with appropriate parameters
    $.ajax({
        url: '/get_data',
        data: {
            location: loc,
            mealperiod: mealperiod
        },
        success: function (data) {
            // Update the content of the data-container div with the received data
            console.log(data);
            return updateFoodItems(mealperiod, data);
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });
}

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

    window.location = this.action + '?' + params.toString();
});
