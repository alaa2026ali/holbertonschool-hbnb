/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

/* =========================
   LOGIN
========================= */

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

                    document.cookie =
                        `token=${data.access_token}; path=/`;

                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();

                    alert(
                        'Login failed: ' +
                        (error.message || error.msg || 'Unknown error')
                    );
                }
            } catch (error) {
                alert('An error occurred while logging in.');
                console.error(error);
            }
        });
    }
});


/* =========================
   COOKIES
========================= */

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


/* =========================
   AUTHENTICATION
========================= */

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


/* =========================
   PLACES
========================= */

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
        console.error(
            'Error fetching places:',
            error
        );
    }
}


function displayPlaces(places) {
    const placesList =
        document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard =
            document.createElement('article');

        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h2>${place.title}</h2>

            <p>
                Price per night: $${place.price}
            </p>

            <p>
                ${place.description}
            </p>

            <a
                href="place.html?id=${encodeURIComponent(place.id)}"
                class="details-button"
            >
                View Details
            </a>
        `;

        placesList.appendChild(placeCard);
    });
}


/* =========================
   PRICE FILTER
========================= */

function setupPriceFilter() {
    const priceFilter =
        document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const prices = [10, 50, 100, 'All'];

    priceFilter.innerHTML = '';

    prices.forEach(price => {
        const option =
            document.createElement('option');

        option.value = price;

        option.textContent =
            price === 'All'
                ? 'All'
                : `$${price}`;

        priceFilter.appendChild(option);
    });
}


function filterPlaces() {
    const priceFilter =
        document.getElementById('price-filter');

    if (!priceFilter) {
        return;
    }

    const selectedPrice =
        priceFilter.value;

    const placeCards =
        document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price =
            parseFloat(card.dataset.price);

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


/* =========================
   URL / PLACE ID
========================= */

function getPlaceIdFromURL() {
    const params =
        new URLSearchParams(window.location.search);

    return params.get('id');
}


/* =========================
   PLACE DETAILS
========================= */

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
            const place =
                await response.json();

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

    const reviewLink =
        document.getElementById('add-review-link');

    if (!placeId) {
        console.error(
            'Place ID is missing from URL'
        );

        return;
    }

    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }

    if (reviewLink && token) {
        const reviewUrl =
            `add_review.html?id=${encodeURIComponent(placeId)}`;

        reviewLink.href = reviewUrl;

        console.log(
            'Review URL:',
            reviewUrl
        );
    }

    fetchPlaceDetails(token, placeId);
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

            <p>
                <strong>Amenities:</strong>
            </p>

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


/* =========================
   REVIEWS - GET
========================= */

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
            const reviews =
                await response.json();

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
    const reviewsSection =
        document.getElementById('reviews');

    if (!reviewsSection) {
        return;
    }

    reviewsSection.innerHTML =
        '<h2>Reviews</h2>';

    reviews.forEach(review => {
        const reviewCard =
            document.createElement('article');

        reviewCard.className =
            'review-card';

        reviewCard.innerHTML = `
            <p>
                <strong>User:</strong>
                ${review.user_id}
            </p>

            <p>
                ${review.text}
            </p>

            <p>
                Rating: ${review.rating}/5
            </p>
        `;

        reviewsSection.appendChild(reviewCard);
    });
}


/* =========================
   GET USER ID FROM JWT
========================= */

function getUserIdFromToken(token) {
    try {
        const parts = token.split('.');

        if (parts.length !== 3) {
            console.error('Invalid JWT token');
            return null;
        }

        const payload = parts[1];

        const decodedPayload = JSON.parse(
            atob(
                payload
                    .replace(/-/g, '+')
                    .replace(/_/g, '/')
            )
        );

        console.log('JWT payload:', decodedPayload);

        return decodedPayload.sub;

    } catch (error) {
        console.error(
            'Failed to decode token:',
            error
        );

        return null;
    }
}


/* =========================
   SUBMIT REVIEW
========================= */

async function submitReview(
    token,
    placeId,
    reviewText,
    rating
) {
    const userId = getUserIdFromToken(token);

    if (!userId) {
        alert('Unable to identify the current user.');
        return false;
    }

    if (!placeId) {
        alert('Place ID is missing.');
        return false;
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

        console.log(
            'Review response status:',
            response.status
        );

        const data = await response.json();

        console.log(
            'Review response:',
            data
        );

        if (response.ok) {
            alert('Review submitted successfully!');

            window.location.href =
                `place.html?id=${encodeURIComponent(placeId)}`;

            return true;
        }

        alert(
            'Failed to submit review: ' +
            (
                data.message ||
                data.msg ||
                data.error ||
                'Unknown error'
            )
        );

        return false;

    } catch (error) {
        console.error(
            'Error submitting review:',
            error
        );

        alert(
            'An error occurred while submitting the review.'
        );

        return false;
    }
}


/* =========================
   REVIEW FORM
========================= */

function setupReviewForm() {

    const reviewForm =
        document.getElementById('review-form');

    if (!reviewForm) {
        return;
    }

    const token =
        getCookie('token');

    if (!token) {
        alert('Please login first.');

        window.location.href =
            'login.html';

        return;
    }

    const placeId =
        getPlaceIdFromURL();

    console.log(
        'Place ID from URL:',
        placeId
    );

    if (!placeId) {
        alert('Place ID is missing.');

        return;
    }

    reviewForm.addEventListener(
        'submit',
        async function(event) {

            event.preventDefault();

            const reviewInput =
                document.getElementById('review');

            const ratingInput =
                document.getElementById('rating');

            if (!reviewInput || !ratingInput) {
                console.error(
                    'Review or rating input not found.'
                );

                return;
            }

            const reviewText =
                reviewInput.value.trim();

            const rating =
                ratingInput.value;

            if (!reviewText) {
                alert(
                    'Please enter a review.'
                );

                return;
            }

            if (!rating) {
                alert(
                    'Please select a rating.'
                );

                return;
            }

            console.log(
                'Submitting review with:'
            );

            console.log(
                'Place ID:',
                placeId
            );

            console.log(
                'Rating:',
                rating
            );

            console.log(
                'Review:',
                reviewText
            );

            const success =
                await submitReview(
                    token,
                    placeId,
                    reviewText,
                    rating
                );

            if (success) {
                reviewForm.reset();
            }
        }
    );
}
/* =========================
   REVIEW FORM
========================= */

function setupReviewForm() {
    const reviewForm =
        document.getElementById('review-form');

    if (!reviewForm) {
        return;
    }

    const token =
        getCookie('token');

    if (!token) {
        window.location.href =
            'index.html';

        return;
    }

    const placeId =
        getPlaceIdFromURL();

    console.log(
        'Place ID from URL:',
        placeId
    );

    console.log(
        'Current URL:',
        window.location.href
    );

    if (!placeId) {
        alert(
            'Place ID is missing.'
        );

        return;
    }

    reviewForm.addEventListener(
        'submit',
        async (event) => {

            event.preventDefault();

            const reviewInput =
                document.getElementById('review');

            const ratingInput =
                document.getElementById('rating');

            if (!reviewInput || !ratingInput) {
                console.error(
                    'Review or rating input not found.'
                );

                return;
            }

            const reviewText =
                reviewInput.value.trim();

            const rating =
                ratingInput.value;

            if (!reviewText || !rating) {
                alert(
                    'Please enter a review and select a rating.'
                );

                return;
            }

            console.log(
                'Submitting review...'
            );

            console.log(
                'Place ID:',
                placeId
            );

            console.log(
                'Rating:',
                rating
            );

            console.log(
                'Review:',
                reviewText
            );

            const success =
                await submitReview(
                    token,
                    placeId,
                    reviewText,
                    rating
                );

            if (success) {
                reviewForm.reset();
            }
        }
    );
}


/* =========================
   PAGE INITIALIZATION
========================= */

document.addEventListener(
    'DOMContentLoaded',
    () => {

        /*
         * Login page
         */
        if (
            document.getElementById(
                'login-form'
            )
        ) {
            return;
        }


        /*
         * Home page
         */
        if (
            document.getElementById(
                'places-list'
            )
        ) {
            setupPriceFilter();

            checkAuthentication();

            const priceFilter =
                document.getElementById(
                    'price-filter'
                );

            if (priceFilter) {
                priceFilter.addEventListener(
                    'change',
                    filterPlaces
                );
            }
        }


        /*
         * Place details page
         */
        if (
            document.getElementById(
                'place-details'
            )
        ) {
            checkPlaceAuthentication();
        }


        /*
         * Add review page
         */
        if (
            document.getElementById(
                'review-form'
            )
        ) {
            setupReviewForm();
        }
    }
);
