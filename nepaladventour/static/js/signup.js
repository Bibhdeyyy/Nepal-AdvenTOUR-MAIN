function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    var icon = document.querySelector(`#${inputId} + i`);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    } else {
        passwordInput.type = "password";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    }
    }



function toggleConfirmPasswordVisibility() {
    var confirmPasswordInput = document.getElementById('confirmpassword');
    var showConfirmPasswordCheckbox = document.getElementById('showConfirmPassword');

    if (showConfirmPasswordCheckbox.checked) {
        confirmPasswordInput.type = 'text';
    } else {
        confirmPasswordInput.type = 'password';
    }
}

function updateFileName(input) {
    var fileName = input.files[0].name;
    var fileNameElement = document.getElementById('file-name');
    fileNameElement.textContent = fileName;
}

// Function to toggle visibility of the social media input
  function toggleSocialMediaInput() {
    var connectDropdown = document.getElementById('connect');
    var socialMediaInput = document.getElementById('social-media-input');

    if (connectDropdown.value === 'Yes') {
        socialMediaInput.style.display = 'block';
    } else {
        socialMediaInput.style.display = 'none';
    }
}

//Function to check password and display error message if passwords not match
function checkPasswords() {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmpassword').value;
    var error = document.getElementById('password-error');

    if (password !== confirmPassword) {
        error.style.display = 'block';
    } else {
        error.style.display = 'none';
    }
}