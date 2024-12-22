const BASE_URL = 'http://localhost:8000/api/'

async function signup() {
    console.log("Signup function called");
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    var email = document.getElementById('email').value;

    const url = `${BASE_URL}auth/signup/`;

    const data = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password,
        password_2: confirmPassword
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        const jsonResponse = await response.json();

        firstNameError = document.getElementById('error-first-name')
        lastNameError = document.getElementById('error-last-name')
        emailError = document.getElementById('error-email')
        passwordError = document.getElementById('error-password')
        password2Error = document.getElementById('error-password-2')
        errorMessage = document.getElementById('error-message')
        successMessage = document.getElementById('success-message')

            
        if (response.ok) {
            console.log(jsonResponse);
            clearErrorFields(firstNameError,
                lastNameError, 
                emailError,
                passwordError, 
                password2Error,
                errorMessage,
                successMessage)
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('success-message').textContent = `წარმატებული რეგისტრაცია, გთხოვთ შეამოწმოთ ელ.ფოსტა ანგარიშის გასააქტიურებლად!`;
        } else {
            clearErrorFields(firstNameError,
                lastNameError, 
                emailError,
                passwordError, 
                password2Error,
                errorMessage,
                successMessage)
            
            if (jsonResponse.first_name) {
                firstNameError.style.display = 'block';
                firstNameError.textContent = jsonResponse.first_name[0];
            }
            if (jsonResponse.last_name) {
                lastNameError.style.display = 'block';
                lastNameError.textContent = jsonResponse.last_name[0];
            }
            if (jsonResponse.email) {
                emailError.style.display = 'block';
                emailError.textContent = jsonResponse.email[0];
            }
            if (jsonResponse.password) {
                passwordError.style.display = 'block';
                passwordError.textContent = jsonResponse.password[0];
            }
            if (jsonResponse.password_2) {
                password2Error.style.display = 'block';
                password2Error.textContent = jsonResponse.password_2[0];
            }
            if (jsonResponse.non_field_errors) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = jsonResponse.non_field_errors[0];
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`შეცდომა: ${error.message}`);
    }
}

function clearErrorFields(firstNameError,
                        lastNameError, 
                        emailError,
                        passwordError, 
                        password2Error,
                        errorMessage,
                        successMessage) {
    if (firstNameError.style) {
        firstNameError.style.display = 'none';
    }
    if (lastNameError.style) {
        lastNameError.style.display = 'none';
    }
    if (emailError.style) {
        emailError.style.display = 'none';
    }
    if (passwordError.style) {
        passwordError.style.display = 'none';
    }
    if (password2Error.style) {
        password2Error.style.display = 'none';
    }
    if (errorMessage.style) {
        errorMessage.style.display = 'none';
    }
    if (successMessage.style) {
        successMessage.style.display = 'none';
    }
}        

async function login(dashboardUrl) {
    console.log("Login function called");
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const url = `${BASE_URL}auth/login/`;

    try {
        console.log("pre-request sent to login")
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password
            })
        });
        console.log("request sent to login")

        const data = await response.json(); 

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            console.log("both cookies written");
            
            window.location.href = dashboardUrl;
            
        } else {
            console.log(data);
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('error-message').textContent = `არასწორი ელ-ფოსტა ან პაროლი, სცადეთ თავიდან!`;
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`An error occurred: ${error.message}`);
    }
}

async function sendLink() {
    console.log("send link function called")
    var email = document.getElementById('email').value;

    const url = `${BASE_URL}auth/reset-password-request/`;
    
    try {
        errorMessage = document.getElementById('error-message')
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email
            })
        });
        const data = await response.json();
        console.log(data);
        
        if (response.ok) {
            if (errorMessage.style) {
                errorMessage.style.display = 'none'
            }
            errorMessage.style.display = 'block';
            errorMessage.style.color = 'green';
            errorMessage.textContent = data.message;
        } else {
            if (errorMessage.style) {
                errorMessage.style.color = 'red';
                errorMessage.style.display = 'none'
            }
            if (data.email) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = data.email[0];
            }
        }
    } catch(err) {
        console.log(err);
    }

}

async function resetPassword(event, loginUrl) {
    console.log('Reset password called');
    event.preventDefault();
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
    var urlParts = window.location.pathname.split('/');
    var uidb64 = urlParts[urlParts.length - 2]; 
    var token = urlParts[urlParts.length - 1];

    const url = `${BASE_URL}auth/reset-password/${uidb64}/${token}/`;

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                password: password,
                password_2: confirmPassword
            })
        });
        
        passwordError = document.getElementById('error-password');
        password2Error = document.getElementById('error-password-2');
        errorMessage = document.getElementById('error-message');
        successMessage = document.getElementById('success-message');

        const data = await response.json();
        console.log(data);
        
        if (response.ok) {
            clearPasswordErrorFields(passwordError, 
                password2Error,
                errorMessage,
                successMessage);
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('success-message').textContent = data.message;
            
            window.location.href = loginUrl;
        } else {
            clearPasswordErrorFields(passwordError, 
                            password2Error,
                            errorMessage,
                            successMessage);
            if (data.password) {
                passwordError.style.display = 'block';
                passwordError.textContent = data.password[0];
            }
            if (data.password_2) {
                password2Error.style.display = 'block';
                password2Error.textContent = data.password_2[0];
            }
            if (data.non_field_errors) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = data.non_field_errors[0];
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function clearPasswordErrorFields(passwordError, 
                                password2Error,
                                errorMessage,
                                successMessage) {
    if (passwordError.style) {
        passwordError.style.display = 'none';
    }
    if (password2Error.style) {
        password2Error.style.display = 'none';
    }
    if (errorMessage.style) {
        errorMessage.style.display = 'none';
    }
    if (successMessage.style) {
        successMessage.style.display = 'none';
    }   
}

