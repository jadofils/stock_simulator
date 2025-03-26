//login.html 

    document.getElementById("login-form").addEventListener("submit", function(e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch('/api/v1/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.detail === "Login successful.") {
                alert("Login successful!");
                // Redirect to the dashboard or homepage
            } else {
                alert("Invalid credentials.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
//on click redirect to login page
    
document.getElementById("login").addEventListener("click", function() {
    // Check if the current URL contains the login API endpoint
    const url = "/api/v1/login";  // Use relative URL path instead of full URL
    if (window.location.pathname.includes(url)) {
        // Redirect to the login page
        window.location.href = `${url}`;
    } else {
        alert('Please check your location');
    }
});
// Handle Forgot Password redirection
document.getElementById("forgot-password-link").addEventListener("click", function(event) {
    event.preventDefault();  // Prevent default link action
    window.location.href = "/api/v1/forgot_password/";  // Redirect to Forgot Password page
});

// Handle Sign Up redirection
document.getElementById("signup-link").addEventListener("click", function(event) {
    event.preventDefault();  
    window.location.href = "/api/v1/signup/";  
});
