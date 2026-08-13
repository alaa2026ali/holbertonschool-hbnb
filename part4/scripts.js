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
                'https://web-5000-195-68.cod-eu-west-3.hbtn.io/api/v1/auth/login',
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
