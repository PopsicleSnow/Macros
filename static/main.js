// Function to fetch and display data
function fetchMealperiods(loc) {
    // Make an AJAX request to /mealperiods endpoint with appropriate parameters
    $.ajax({
        url: '/mealperiods',
        data: {
            location: loc
        },
        success: function (data) {
            // Update the content with the received data
            data.forEach(function (mealPeriod) {
                $('#mealperiods').append(`<li><a class="dropdown-item" href="#">${mealPeriod}</a></li>`);
            })
        },
        error: function (error) {
            console.log('Error fetching data:', error);
        }
    });
}

function updateFoodItems(mealPeriod, data) {
    // Update the prompt
    $('#prompt').html(`What did you eat during ${mealPeriod}?`);
    
    // Hide meal selection and show food form
    $('#meal-selection').fadeOut(300, function() {
        $('#foodStuff').removeClass('d-none').html(
            '<div class="row justify-content-center">' +
            '<div class="col-12 col-lg-8">' +
            '<div class="main-card">' +
            '<h2 class="h4 mb-4 text-center">Select Your Food Items</h2>' +
            '<form id="foodForm" action="/result" method="POST">' +
            '<div id="fooditems" class="mb-4"></div>' +
            '</form>' +
            '<div class="text-center">' +
            '<button form="foodForm" type="submit" class="btn btn-primary btn-lg px-5">Calculate My Macros</button>' +
            '<p class="mt-3 small text-muted"><em>*Each serving size is equivalent to 1 piece/slice/scoop</em></p>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '</div>'
        ).hide().fadeIn(400);
        
        // Process and add food items
        populateFoodItems(data);
    });
}

function populateFoodItems(data) {
    // Check if we have data
    if (!data || data.length === 0) {
        $('#fooditems').html('<p class="text-center text-muted">No food items available for this meal period.</p>');
        return;
    }
    
    // Sort data by category for better organization
    data.sort(function(a, b) {
        if (a.category !== b.category) {
            return a.category.localeCompare(b.category);
        }
        return a.name.localeCompare(b.name);
    });
    
    let currentCategory = '';
    data.forEach(function (foodItem) {
        const name = foodItem.name;
        const category = foodItem.category || 'Other';
        
        // Add category header if it's a new category
        if (category !== currentCategory) {
            currentCategory = category;
            $('#fooditems').append(`
                <div class="category-header mt-4 mb-3">
                    <h5 class="text-primary border-bottom border-primary pb-2">${category}</h5>
                </div>
            `);
        }
        
        // Create food item with compact styling
        $('#fooditems').append(`
            <div class="food-item mb-2">
                <label for="${name}" class="form-label mb-1">${name}</label>
                <div class="input-group mb-2">
                    <input type="number" name="${name}" step="any" min="0" max="${MAX_SERVINGS}" 
                           aria-label="${name}" class="form-control" id="${name}" 
                           placeholder="Servings (${foodItem.servingSize})">
                    <button class="btn btn-outline-secondary add-one-btn" type="button">+1</button>
                    <input type="hidden" name="${name}" value="${foodItem.calories}">
                    <input type="hidden" name="${name}" value="${foodItem.fat}">
                    <input type="hidden" name="${name}" value="${foodItem.carbs}">
                    <input type="hidden" name="${name}" value="${foodItem.protein}">
                    <input type="hidden" name="${name}" value="${foodItem.sugar}">
                </div>
            </div>
        `);
    });
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
            // Update the content with the received data
            updateFoodItems(mealperiod, data);
        },
        error: function (error) {
            console.log('Error fetching data:', error);
            // Show error message
            $('#meal-selection').fadeOut(300, function() {
                $('#foodStuff').removeClass('d-none').html(
                    '<div class="row justify-content-center">' +
                    '<div class="col-12 col-lg-6">' +
                    '<div class="main-card text-center">' +
                    '<h5 class="text-danger mb-3">Error Loading Menu</h5>' +
                    '<p class="text-muted mb-3">There was a problem loading the menu items. Please try again.</p>' +
                    '<button class="btn btn-secondary" onclick="location.reload()">Retry</button>' +
                    '</div>' +
                    '</div>' +
                    '</div>'
                ).hide().fadeIn(400);
            });
        }
    });
}

// Constants
const MAX_SERVINGS = 50;

$(document).ready(function () {
    // Add event listener for +1 buttons (using delegated event listener)
    $(document).on('click', '.add-one-btn', function() {
        const input = $(this).siblings('input[type="number"]');
        const currentValue = parseFloat(input.val()) || 0;
        
        if (currentValue < MAX_SERVINGS) {
            input.val(currentValue + 1);
        }
    });

    // Form submission handler - using event delegation for dynamically created forms
    $(document).on('submit', '#foodForm', function(event) {
        event.preventDefault();
        
        const params = new URLSearchParams();
        const invalidNames = new Set();
        const validNames = new Set();
        
        for (const input of this.elements) {
            if (invalidNames.has(input.name)) continue;
            
            if (!validNames.has(input.name) && !invalidNames.has(input.name) && 
                (input.value <= 0 || input.value === '')) {
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
        })
        .then(response => response.text())
        .then(html => {
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => {
            console.log('Error:', error);
        });
    });
});
