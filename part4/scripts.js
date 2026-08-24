const API_URL =
    'https://web-5000-77-207.cod-eu-west-3.hbtn.io/api/v1';


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


/* Login */

document.addEventListener('DOMContentLoaded', () => {

    const loginForm =
        document.getElementById('login-form');

    if (loginForm) {

        loginForm.addEventListener(
            'submit',
            async (e) => {

                e.preventDefault();

                const email =
                    document.getElementById(
                        'email'
                    ).value;

                const password =
                    document.getElementById(
                        'password'
                    ).value;

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
            }
        );

        return;
    }


    /* Home */

    const placesList =
        document.getElementById(
            'places-list'
        );

    if (placesList) {

        const token =
            getCookie('token');

        const loginLink =
            document.getElementById(
                'login-link'
            );

        setupPriceFilter();

        if (!token) {

            if (loginLink) {
                loginLink.style.display =
                    'block';
            }

            return;
        }

        if (loginLink) {
            loginLink.style.display =
                'none';
        }

        fetch(
            `${API_URL}/places/`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        )
        .then(response => response.json())
        .then(places => {
            displayPlaces(places);
        })
        .catch(error => {
            console.error(error);
        });
    }


    /* Place details */

    const placeDetails =
        document.getElementById(
            'place-details'
        );

    if (placeDetails) {

        const token =
            getCookie('token');

        const placeId =
            getPlaceId();

        fetch(
            `${API_URL}/places/${placeId}`,
            {
                headers: token
                    ? {
                        Authorization:
                            `Bearer ${token}`
                    }
                    : {}
            }
        )
        .then(response => response.json())
        .then(place => {

            displayPlace(place);

            fetchReviews(
                placeId,
                token
            );
        });
    }


    /* Review */

    const reviewForm =
        document.getElementById(
            'review-form'
        );

    if (reviewForm) {
        setupReviewForm(reviewForm);
    }
});


/* Display Places */

function displayPlaces(places) {

    const list =
        document.getElementById(
            'places-list'
        );

    if (!list) {
        return;
    }

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

        list.innerHTML += `
            <article
                class="place-card"
                data-price="${place.price}"
            >

                <img
                    src="${images[place.title]}"
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


/* Price Filter */

function setupPriceFilter() {

    const filter =
        document.getElementById(
            'price-filter'
        );

    if (!filter) {
        return;
    }


    [10, 50, 100, 'All'].forEach(
        price => {

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
        }
    );


    filter.addEventListener(
        'change',
        () => {

            document
                .querySelectorAll(
                    '.place-card'
                )
                .forEach(card => {

                    const price =
                        parseFloat(
                            card.dataset.price
                        );

                    card.style.display =
                        filter.value === 'All' ||
                        price <=
                        parseFloat(
                            filter.value
                        )
                            ? 'block'
                            : 'none';
                });
        }
    );
}


/* Place Details */

function displayPlace(place) {

    document.getElementById(
        'place-details'
    ).innerHTML = `

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
                place.amenities?.length
                    ? place.amenities
                        .map(
                            a =>
                                `<li>
                                    ${a.name || a}
                                </li>`
                        )
                        .join('')
                    : '<li>No amenities listed</li>'
            }
        </ul>
    `;
}


/* Reviews */

async function fetchReviews(
    placeId,
    token
) {

    try {

        const response =
            await fetch(
                `${API_URL}/places/${placeId}/reviews`,
                {
                    headers: token
                        ? {
                            Authorization:
                                `Bearer ${token}`
                        }
                        : {}
                }
            );

        const reviews =
            await response.json();

        displayReviews(reviews);

    } catch (error) {

        console.error(error);
    }
}


/* Display Reviews */

function displayReviews(reviews) {

    const section =
        document.getElementById(
            'reviews'
        );

    if (!section) {
        return;
    }

    section.innerHTML =
        '<h2>Reviews</h2>';


    if (!reviews.length) {

        section.innerHTML +=
            '<p>No reviews yet.</p>';

        return;
    }


    reviews.forEach(review => {

        section.innerHTML += `

            <article
                class="review-card"
            >

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


/* Review Form */

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
        async e => {

            e.preventDefault();


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

                                Authorization:
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


                if (!response.ok) {

                    const data =
                        await response.json();

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
