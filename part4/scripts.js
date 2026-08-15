/*
  HBnB - Simple Web Client
  scripts.js
*/

/* =========================
   API
========================= */

const API_URL =
    'https://web-5000-65-220.cod-eu-west-3.hbtn.io/api/v1';


/* =========================
   LOGIN
========================= */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(
                `${API_URL}/auth/login`,
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

            const data = await response.json();

            if (response.ok) {
                document.cookie =
                    `token=${data.access_token}; path=/`;

                window.location.href = 'index.html';
            } else {
                alert(
                    'Login failed: ' +
                    (
                        data.message ||
                        data.msg ||
                        'Invalid email or password'
                    )
                );
            }

        } catch (error) {
            console.error('Login error:', error);

            alert(
                'An error occurred while logging in.'
            );
        }
    });
});


/* =========================
   COOKIE
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
   GET USER ID FROM JWT
========================= */

function getUserIdFromToken(token) {
    try {
        if (!token) {
            return null;
        }

        const parts = token.split('.');

        if (parts.length !== 3) {
            console.error('Invalid JWT token');
            return null;
        }

        let payload = parts[1];

        /*
         * Fix Base64URL padding
         */
        payload = payload
            .replace(/-/g, '+')
            .replace(/_/g, '/');

        while (payload.length % 4) {
            payload += '=';
        }

        const decodedPayload =
            JSON.parse(atob(payload));

        console.log(
            'JWT payload:',
            decodedPayload
        );

        return decodedPayload.sub || null;

    } catch (error) {
        console.error(
            'Failed to decode token:',
            error
        );

        return null;
    }
}


/* =========================
   HOME PAGE AUTHENTICATION
========================= */

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink =
        document.getElementById('login-link');

    if (!loginLink) {
        return;
    }

    if (!token) {
        loginLink.style.display = 'block';
        return;
    }

    loginLink.style.display = 'none';

    fetchPlaces(token);
}


/* =========================
   FETCH PLACES
========================= */

async function fetchPlaces(token) {
    try {
        const response = await fetch(
            `${API_URL}/places/`,
            {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            console.error(
                'Failed to fetch places:',
                response.status
            );
            return;
        }

        const places = await response.json();

        displayPlaces(places);

    } catch (error) {
        console.error(
            'Error fetching places:',
            error
        );
    }
}


/* =========================
   DISPLAY PLACES
========================= */

function displayPlaces(places) {
    const placesList =
        document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach((place) => {
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

    const prices = [
        10,
        50,
        100,
        'All'
    ];

    priceFilter.innerHTML = '';

    prices.forEach((price) => {
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

    placeCards.forEach((card) => {
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
   GET PLACE ID
========================= */

function getPlaceIdFromURL() {
    const params =
        new URLSearchParams(
            window.location.search
        );

    const placeId =
        params.get('id');

    console.log(
        'URL:',
        window.location.href
    );

    console.log(
        'Place ID:',
        placeId
    );

    return placeId;
}


/* =========================
   PLACE DETAILS
========================= */

async function fetchPlaceDetails(
    token,
    placeId
) {
    try {
        const headers = {};

        if (token) {
            headers['Authorization'] =
                `Bearer ${token}`;
        }

        const response = await fetch(
            `${API_URL}/places/${encodeURIComponent(placeId)}`,
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            console.error(
                'Failed to fetch place:',
                response.status
            );
            return;
        }

        const place =
            await response.json();

        displayPlaceDetails(place);

        fetchReviews(
            placeId,
            token
        );

    } catch (error) {
        console.error(
            'Error fetching place details:',
            error
        );
    }
}


/* =========================
   PLACE AUTHENTICATION
========================= */

function checkPlaceAuthentication() {
    const token =
        getCookie('token');

    const placeId =
        getPlaceIdFromURL();

    const addReviewSection =
        document.getElementById(
            'add-review'
        );

    const reviewLink =
        document.getElementById(
            'add-review-link'
        );

    if (!placeId) {
        console.error(
            'Place ID is missing from URL.'
        );

        return;
    }

    /*
     * Show/hide review section
     */
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display =
                'block';
        } else {
            addReviewSection.style.display =
                'none';
        }
    }

    /*
     * IMPORTANT:
     * Send the place ID to add_review.html
     */
    if (reviewLink && token) {
        const reviewUrl =
            `add_review.html?id=${encodeURIComponent(placeId)}`;

        reviewLink.href = reviewUrl;

        console.log(
            'Review URL:',
            reviewUrl
        );
    }

    fetchPlaceDetails(
        token,
        placeId
    );
}


/* =========================
   DISPLAY PLACE DETAILS
========================= */

function displayPlaceDetails(place) {
    const placeDetails =
        document.getElementById(
            'place-details'
        );

    if (!placeDetails) {
        return;
    }

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>

        <div class="place-info">

            <p>
                <strong>
                    Price per night:
                </strong>

                $${place.price}
            </p>

            <p>
                <strong>
                    Description:
                </strong>

                ${place.description}
            </p>

            <p>
                <strong>
                    Amenities:
                </strong>
            </p>

            <ul>
                ${
                    place.amenities &&
                    place.amenities.length
                        ? place.amenities
                            .map(
                                (amenity) => `
                                    <li>
                                        ${
                                            amenity.name ||
                                            amenity
                                        }
                                    </li>
                                `
                            )
                            .join('')
                        : `
                            <li>
                                No amenities listed
                            </li>
                        `
                }
            </ul>

        </div>
    `;
}


/* =========================
   FETCH REVIEWS
========================= */

async function fetchReviews(
    placeId,
    token
) {
    try {
        const headers = {};

        if (token) {
            headers['Authorization'] =
                `Bearer ${token}`;
        }

        const response = await fetch(
            `${API_URL}/places/${encodeURIComponent(placeId)}/reviews`,
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            console.error(
                'Failed to fetch reviews:',
                response.status
            );

            return;
        }

        const reviews =
            await response.json();

        displayReviews(reviews);

    } catch (error) {
        console.error(
            'Error fetching reviews:',
            error
        );
    }
}


/* =========================
   DISPLAY REVIEWS
========================= */

function displayReviews(reviews) {
    const reviewsSection =
        document.getElementById(
            'reviews'
        );

    if (!reviewsSection) {
        return;
    }

    reviewsSection.innerHTML =
        '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += `
            <p>
                No reviews yet.
            </p>
        `;

        return;
    }

    reviews.forEach((review) => {
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
                Rating:
                ${review.rating}/5
            </p>
        `;

        reviewsSection.appendChild(
            reviewCard
        );
    });
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
    console.log(
        '========== SUBMIT REVIEW =========='
    );

    console.log(
        'Place ID:',
        placeId
    );

    console.log(
        'Review:',
        reviewText
    );

    console.log(
        'Rating:',
        rating
    );

    const userId =
        getUserIdFromToken(token);

    console.log(
        'User ID:',
        userId
    );

    if (!userId) {
        alert(
            'Unable to identify the current user.'
        );

        return false;
    }

    if (!placeId) {
        alert(
            'Place ID is missing.'
        );

        return false;
    }

    try {
        const response = await fetch(
            `${API_URL}/reviews/`,
            {
                method: 'POST',

                headers: {
                    'Content-Type':
                        'application/json',

                    'Authorization':
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    text: reviewText,

                    rating:
                        parseInt(
                            rating,
                            10
                        ),

                    user_id:
                        userId,

                    place_id:
                        placeId
                })
            }
        );

        console.log(
            'Response status:',
            response.status
        );

        const data =
            await response.json();

        console.log(
            'Response data:',
            data
        );

        if (response.ok) {
            alert(
                'Review submitted successfully!'
            );

            /*
             * Return to the same place
             */
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
        document.getElementById(
            'review-form'
        );

    if (!reviewForm) {
        return;
    }

    const token =
        getCookie('token');

    if (!token) {
        alert(
            'Please login first.'
        );

        window.location.href =
            'login.html';

        return;
    }

    /*
     * Get ID from:
     * add_review.html?id=PLACE_ID
     */
    const placeId =
        getPlaceIdFromURL();

    console.log(
        'Review page Place ID:',
        placeId
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
                document.getElementById(
                    'review'
                );

            const ratingInput =
                document.getElementById(
                    'rating'
                );

            if (!reviewInput) {
                console.error(
                    'Review input not found.'
                );

                return;
            }

            if (!ratingInput) {
                console.error(
                    'Rating input not found.'
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
                'Submitting review...'
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
         * LOGIN PAGE
         */
        if (
            document.getElementById(
                'login-form'
            )
        ) {
            return;
        }


        /*
         * HOME PAGE
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
         * PLACE PAGE
         */
        if (
            document.getElementById(
                'place-details'
            )
        ) {
            checkPlaceAuthentication();
        }


        /*
         * ADD REVIEW PAGE
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
