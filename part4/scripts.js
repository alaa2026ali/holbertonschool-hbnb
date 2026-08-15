/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(
                    'https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1/auth/login',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

                if (response.ok) {
                    const data = await response.json();

                    document.cookie = `token=${data.access_token}; path=/`;

                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    alert('Login failed: ' + error.message);
                }
            } catch (error) {
                alert('An error occurred while logging in.');
                console.error(error);
            }
        });
    }
});


function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) {
        return;
    }

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}


async function fetchPlaces(token) {
    try {
        const response = await fetch(
            'https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1/places/',
            {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error(
                'Failed to fetch places:',
                response.status
            );
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('article');

        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <p>${place.description}</p>
            <a href="place.html?id=${place.id}" class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(placeCard);
    });
}


function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const prices = [10, 50, 100, 'All'];

    priceFilter.innerHTML = '';

    prices.forEach(price => {
        const option = document.createElement('option');

        option.value = price;
        option.textContent =
            price === 'All' ? 'All' : `$${price}`;

        priceFilter.appendChild(option);
    });
}


function filterPlaces() {
    const priceFilter = document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const selectedPrice = priceFilter.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);

        if (
            selectedPrice === 'All' ||
            price <= parseFloat(selectedPrice)
        ) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(
            `https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1/places/${placeId}`,
            {
                method: 'GET',
                headers: token
                    ? {
                        'Authorization': `Bearer ${token}`
                    }
                    : {}
            }
        );

        if (response.ok) {
            const place = await response.json();

            displayPlaceDetails(place);

            fetchReviews(placeId, token);
        } else {
            console.error(
                'Failed to fetch place details:',
                response.status
            );
        }
    } catch (error) {
        console.error(
            'Error fetching place details:',
            error
        );
    }
}


function checkPlaceAuthentication() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    const addReviewSection =
        document.getElementById('add-review');

    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }

    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
}


function displayPlaceDetails(place) {
    const placeDetails =
        document.getElementById('place-details');

    if (!placeDetails) {
        return;
    }

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>

        <div class="place-info">
            <p>
                <strong>Price per night:</strong>
                $${place.price}
            </p>

            <p>
                <strong>Description:</strong>
                ${place.description}
            </p>

            <p><strong>Amenities:</strong></p>

            <ul>
                ${
                    place.amenities &&
                    place.amenities.length
                        ? place.amenities
                            .map(
                                amenity =>
                                    `<li>${
                                        amenity.name || amenity
                                    }</li>`
                            )
                            .join('')
                        : '<li>No amenities listed</li>'
                }
            </ul>
        </div>
    `;
}


async function fetchReviews(placeId, token) {
    try {
        const response = await fetch(
            `https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1/places/${placeId}/reviews`,
            {
                method: 'GET',
                headers: token
                    ? {
                        'Authorization': `Bearer ${token}`
                    }
                    : {}
            }
        );

        if (response.ok) {
            const reviews = await response.json();

            displayReviews(reviews);
        } else {
            console.error(
                'Failed to fetch reviews:',
                response.status
            );
        }
    } catch (error) {
        console.error(
            'Error fetching reviews:',
            error
        );
    }
}


function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');

    if (!reviewsSection) {
        return;
    }

    reviewsSection.innerHTML = '<h2>Reviews</h2>';

    reviews.forEach(review => {
        const reviewCard = document.createElement('article');

        reviewCard.className = 'review-card';

        reviewCard.innerHTML = `
            <p>
                <strong>User:</strong>
                ${review.user_id}
            </p>

            <p>${review.text}</p>

            <p>
                Rating: ${review.rating}/5
            </p>
        `;

        reviewsSection.appendChild(reviewCard);
    });
}


document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('login-form')) {
        return;
    }

    if (document.getElementById('places-list')) {
        setupPriceFilter();

        checkAuthentication();

        const priceFilter =
            document.getElementById('price-filter');

        if (priceFilter) {
            priceFilter.addEventListener(
                'change',
                filterPlaces
            );
        }
    }

    if (document.getElementById('place-details')) {
        checkPlaceAuthentication();
    }
});
function getUserIdFromToken(token) {
    try {
        const payload = token.split('.')[1];
        const decodedPayload = JSON.parse(
            atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
        );

        return decodedPayload.sub;
    } catch (error) {
        console.error('Failed to decode token:', error);
        return null;
    }
}

async function submitReview(token, placeId, reviewText, rating) {
    const userId = getUserIdFromToken(token);

    if (!userId) {
        alert('Unable to identify the current user.');
        return;
    }

    try {
        const response = await fetch(
            'https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1/reviews/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: parseInt(rating, 10),
                    user_id: userId,
                    place_id: placeId
                })
            }
        );

        if (response.ok) {
            alert('Review submitted successfully!');
            return true;
        }

        const error = await response.json();

        alert(
            'Failed to submit review: ' +
            (error.message || error.msg || 'Unknown error')
        );

        return false;
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting the review.');
        return false;
    }
}

function setupReviewForm() {
    const reviewForm = document.getElementById('review-form');

    if (!reviewForm) {
        return;
    }

    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        alert('Place ID is missing.');
        return;
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText =
            document.getElementById('review').value.trim();

        const rating =
            document.getElementById('rating').value;

        if (!reviewText || !rating) {
            alert('Please enter a review and select a rating.');
            return;
        }

        const success = await submitReview(
            token,
            placeId,
            reviewText,
            rating
        );

        if (success) {
            reviewForm.reset();
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('review-form')) {
        setupReviewForm();
    }
});
