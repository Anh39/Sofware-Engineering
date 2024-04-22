const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const loginPopup = document.querySelector('.login-popup');
const iconClose = document.querySelector('.icon-close');
const LoginButton = document.querySelector('#Login');
const RegisterButton = document.querySelector('#Register');

const inputLoginUsername = document.querySelector(".input-login-username");
const inputLoginPassword = document.querySelector(".input-login-password");

const inputRegisterUsername = document.querySelector(".input-register-username");
const inputRegisterEmail = document.querySelector(".input-register-email");
const inputRegisterPassword = document.querySelector(".input-register-password");

registerLink.addEventListener('click', () => {
    wrapper.classList.add('active');
})

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
})

// loginPopup.addEventListener('click', () => {
//     wrapper.classList.add('active-popup');
// })

iconClose.addEventListener('click', () => {
    // wrapper.classList.remove('active-popup');
    window.location.href = "index.html";
})

LoginButton.addEventListener('click', () => {
    fetch('/authentication/login', {
        method: 'POST',
        body: JSON.stringify({
            'username': inputLoginUsername.value,
            'password': inputLoginPassword.value
        })
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "./index.html";
                return response.json();
            } else {
                console.log("sai");
            }
        })
        .then()
})

RegisterButton.addEventListener('click', () => {
    fetch("/authentication/register", {
        method: 'POST',
        body: JSON.stringify({
            'username': inputRegisterUsername.value,
            'password': inputRegisterPassword.value,
            'email': inputRegisterEmail.value
        })
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "./index.html";
                return response.json();
            } else {
                console.log("sai");
            }
        })
        .then()
})