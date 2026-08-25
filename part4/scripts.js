const API_URL =
    'http://127.0.0.1:5000/api/v1';


function getCookie(name) {
    const cookie = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));

    return cookie ? cookie.split('=')[1] : null;
}


function getPlaceId() {
    return new URLSearchParams(
        window.location.search
    ).get('id');
}


/* =========================
   PAGE LOAD
========================= */

document.addEventListener('DOMContentLoaded', () => {

    /* Login */

    const loginForm =
        document.getElementById('login-form');

    if (loginForm) {
        setupLogin(loginForm);
        return;
    }


    /* Home */

    const placesList =
        document.getElementById('places-list');

    if (placesList) {
        setupPriceFilter();
        fetchPlaces();
    }


    /* Place */

    const placeDetails =
        document.getElementById('place-details');

    if (placeDetails) {
        loadPlace();
    }


    /* Add Review Link */

    const addReviewLink =
        document.getElementById('add-review-link');

    if (addReviewLink) {

        const placeId =
            getPlaceId();

        if (placeId) {

            addReviewLink.href =
                `add_review.html?id=${placeId}`;
        }
    }


    /* Review */

    const reviewForm =
        document.getElementById('review-form');

    if (reviewForm) {
        setupReviewForm(reviewForm);
    }
});


/* =========================
   LOGIN
========================= */

function setupLogin(form) {

    form.addEventListener('submit', async (event) => {

        event.preventDefault();

        const email =
            document.getElementById('email').value.trim();

        const password =
            document.getElementById('password').value;

        try {

            const response =
                await fetch(
                    `${API_URL}/auth/login`,
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                alert(
                    data.msg ||
                    data.message ||
                    'Invalid email or password'
                );

                return;
            }

            document.cookie =
                `token=${data.access_token}; path=/`;

            window.location.href =
                'index.html';

        } catch (error) {

            console.error(error);

            alert('Login failed');
        }
    });
}


/* =========================
   PLACES
========================= */

async function fetchPlaces() {

    try {

        const response =
            await fetch(
                `${API_URL}/places/`
            );

        if (!response.ok) {
            throw new Error(
                'Failed to load places'
            );
        }

        const places =
            await response.json();

        displayPlaces(places);

    } catch (error) {

        console.error(
            'Error loading places:',
            error
        );
    }
}


function displayPlaces(places) {

    const list =
        document.getElementById(
            'places-list'
        );

    if (!list) return;

    list.innerHTML = '';

    const images = {
        "Riyadh Luxury Apartment":
            "images/Riyadh.png",

        "Jeddah Beach House":
            "images/Jeddah Beach House.png",

        "AlUla Desert Villa":
            "images/AlUla Desert Villa.png"
    };


    places.forEach(place => {

        const image =
            images[place.title] ||
            "images/Riyadh.png";

        list.innerHTML += `

            <article
                class="place-card"
                data-price="${place.price}"
            >

                <img
                    src="${image}"
                    alt="${place.title}"
                >

                <h2>
                    ${place.title}
                </h2>

                <p>
                    Price per night:
                    $${place.price}
                </p>

                <p>
                    ${place.description}
                </p>

                <a
                    href="place.html?id=${place.id}"
                    class="details-button"
                >
                    View Details
                </a>

            </article>

        `;
    });
}


/* =========================
   PRICE FILTER
========================= */

function setupPriceFilter() {

    const filter =
        document.getElementById(
            'price-filter'
        );

    if (!filter) return;

    filter.innerHTML = '';

    const prices = [
        10,
        50,
        100,
        'All'
    ];

    prices.forEach(price => {

        const option =
            document.createElement(
                'option'
            );

        option.value = price;

        option.textContent =
            price === 'All'
                ? 'All'
                : `$${price}`;

        filter.appendChild(option);
    });

    filter.addEventListener(
        'change',
        filterPlaces
    );
}


function filterPlaces() {

    const filter =
        document.getElementById(
            'price-filter'
        );

    const selected =
        filter.value;

    const cards =
        document.querySelectorAll(
            '.place-card'
        );

    cards.forEach(card => {

        const price =
            parseFloat(
                card.dataset.price
            );

        if (
            selected === 'All' ||
            price <= parseFloat(selected)
        ) {

            card.style.display =
                'block';

        } else {

            card.style.display =
                'none';
        }
    });
}


/* =========================
   PLACE DETAILS
========================= */

async function loadPlace() {

    const placeId =
        getPlaceId();

    if (!placeId) {
        return;
    }

    const token =
        getCookie('token');

    try {

        const response =
            await fetch(
                `${API_URL}/places/${placeId}`
            );

        if (!response.ok) {

            throw new Error(
                'Place not found'
            );
        }

        const place =
            await response.json();

        displayPlace(place);

        fetchReviews(
            placeId,
            token
        );

    } catch (error) {

        console.error(error);

        document.getElementById(
            'place-details'
        ).innerHTML =
            '<p>Place not found.</p>';
    }
}


function displayPlace(place) {

    const details =
        document.getElementById(
            'place-details'
        );

    if (!details) return;

    details.innerHTML = `

        <h1>
            ${place.title}
        </h1>

        <p>
            <strong>Price:</strong>
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
                                `<li>
                                    ${
                                        amenity.name ||
                                        amenity
                                    }
                                </li>`
                        )
                        .join('')

                    : '<li>No amenities listed</li>'
            }

        </ul>

    `;
}


/* =========================
   REVIEWS
========================= */

async function fetchReviews(
    placeId,
    token
) {

    try {

        const headers = {};

        if (token) {

            headers.Authorization =
                `Bearer ${token}`;
        }

        const response =
            await fetch(
                `${API_URL}/places/${placeId}/reviews`,
                {
                    headers: headers
                }
            );

        if (!response.ok) {
            return;
        }

        const reviews =
            await response.json();

        displayReviews(reviews);

    } catch (error) {

        console.error(
            'Error loading reviews:',
            error
        );
    }
}


function displayReviews(reviews) {

    const section =
        document.getElementById(
            'reviews'
        );

    if (!section) return;

    section.innerHTML =
        '<h2>Reviews</h2>';

    if (!reviews.length) {

        section.innerHTML +=
            '<p>No reviews yet.</p>';

        return;
    }

    reviews.forEach(review => {

        section.innerHTML += `

            <article class="review-card">

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

            </article>

        `;
    });
}


/* =========================
   ADD REVIEW
========================= */

function setupReviewForm(form) {

    const token =
        getCookie('token');

    const placeId =
        getPlaceId();

    if (!token) {

        window.location.href =
            'login.html';

        return;
    }

    form.addEventListener(
        'submit',
        async event => {

            event.preventDefault();

            const text =
                document.getElementById(
                    'review'
                ).value.trim();

            const rating =
                document.getElementById(
                    'rating'
                ).value;

            if (!text || !rating) {

                alert(
                    'Please complete the form'
                );

                return;
            }

            try {

                const payload =
                    JSON.parse(
                        atob(
                            token.split('.')[1]
                        )
                    );

                const response =
                    await fetch(
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

                                text: text,

                                rating:
                                    parseInt(
                                        rating
                                    ),

                                user_id:
                                    payload.sub,

                                place_id:
                                    placeId
                            })
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {

                    alert(
                        data.msg ||
                        data.message ||
                        'Failed to submit review'
                    );

                    return;
                }

                alert(
                    'Review submitted successfully!'
                );

                window.location.href =
                    `place.html?id=${placeId}`;

            } catch (error) {

                console.error(error);

                alert(
                    'Failed to submit review'
                );
            }
        }
    );
}
