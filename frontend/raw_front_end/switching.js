let user_container_visible = false;
let user_visisble = false;
let login_visible = true;
let login_button_visible = true;
function hide_user_container() {
    let user_container = document.getElementById('user_container');
    user_container.style.display = 'none';
    user_container_visible = false;
}
function show_user_container() {
    let user_container = document.getElementById('user_container');
    user_container.style.display = 'flex';
    user_container_visible = true;
}
function hide_user() {
    let user = document.getElementById('user');
    user.style.display = 'none';
    hide_user_container()
    user_visisble = false;
}
function show_user() {
    let user = document.getElementById('user');
    user.style.display = 'flex';
    hide_user_container();
    user_visisble = true;
}
function hide_login() {
    let login_container = document.getElementById('login_container');
    login_container.style.display = 'none';
    login_visible = false;
}
function show_login() {
    let login_container = document.getElementById('login_container');
    login_container.style.display = 'flex';
    login_visible = true;
}  
function hide_login_button() {
    let login_button = document.getElementById('login_button');
    login_button.style.display = 'none';
    login_button_visible = false;
}
function show_login_button() {
    let login_button = document.getElementById('login_button');
    login_button.style.display = 'flex';
    login_button_visible = true;
}
let user_button = document.getElementById('user');
user_button.addEventListener('click', () => {
    if (user_container_visible == true) {
        hide_user_container();
    } else {
        show_user_container();
    }
})
hide_user();
let logout_button = document.getElementById('logout_button');
logout_button.addEventListener('click', () => {
    show_login_button();
    hide_user();
})

function get_cookie(cookie_name) {
    let cookies = document.cookie.split(';');
    for (let i=0;i<cookies.length;i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(cookie_name+'=')) {
            return cookie.substring(cookie_name.length+1);
        }
    }
    return undefined;
} 
function set_cookie(cookie_name,cookie_value) {
    let cookie = cookie_name + '=' + cookie_value + ';' + 'path=/';
    document.cookie = cookie;
}

export{get_cookie,set_cookie,show_user,hide_user,show_login_button,hide_login_button,show_login,hide_login}