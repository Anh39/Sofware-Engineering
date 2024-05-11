import { get_cookie,show_login,show_login_button,show_user,hide_login,hide_login_button,hide_user, set_cookie } from "./switching.js";
import { UserInfo} from "./local.js";
import { TranslateManager } from "./translate_buffer.js";

const langOption = document.querySelectorAll('select');
const fromText = document.querySelector(".fromText");
const transText = document.querySelector(".toTranslate");
const fromVoice = document.querySelector(".from");
const toVoice = document.querySelector(".to");
const cpyBtn = document.querySelector(".bx-copy");
const countValue = document.querySelector(".code_length");
const exchangeLang = document.querySelector(".bx-transfer");

const historyButton = document.querySelector(".history");
const historyBox = document.querySelector(".box-history");
const allContainer = document.querySelector(".all-container");
const boxContainer = document.querySelector(".box-container");
const boxWrapper = document.querySelector(".box-wrapper");

const removeHistoryBox = document.querySelector(".remove-sidebar");

const historyList = document.querySelector("#history-list");

// login.html

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

iconClose.addEventListener('click', () => {
    // wrapper.classList.remove('active-popup');
    allContainer.classList.remove("none-display");
    boxWrapper.classList.remove("block-display");
})
function entry_handler() {
    TranslateManager.text_field = transText;
    let user_info = UserInfo.load_and_get_dict();
    console.log(user_info);
    if (user_info['logged'] == true) {
        show_user();
        hide_login_button();
        hide_login();
        set_cookie('uuid',user_info['uuid']);
    }

    let logout_button = document.getElementById('logout_button');
    logout_button.addEventListener('click', () => {
        UserInfo.clear();
        hide_user();
        show_login_button();
        set_cookie('uuid','');
    })
}
entry_handler();
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
                allContainer.classList.remove("none-display");
                boxWrapper.classList.remove("block-display");
                // console.log(inputLoginUsername.value);
                // return response.json();
                let user_info = UserInfo.load_and_get_dict();
                user_info['name'] = inputLoginUsername.value;
                user_info['logged'] = true;
                user_info['uuid'] = get_cookie('uuid');
                console.log(user_info);
                UserInfo.save_dict(user_info);
                show_user();
                hide_login_button();
                hide_login();
            } else {
                alert("tên đăng nhập hoặc mật khẩu không chính xác");
            }
        })
        .then()
})

// end login

loginPopup.addEventListener("click", () => {
    allContainer.classList.add("none-display");
    boxWrapper.classList.add("block-display");
})

langOption.forEach((get, con) => {
    for (let countryCode in language) {
        let selected;
        if (con == 0 && countryCode == "en-GB") {
            selected = "selected";
        } else if (con == 0 && countryCode == "bn-IN") {
            selected = "selected";
        }

        let option = `<option value="${countryCode}" ${selected}>${language[countryCode]}</option>`;
        get.insertAdjacentHTML('beforeend', option);
    }
})

fromText.addEventListener("input", function () {
    let content = fromText.value;
    let fromContent = langOption[0].value;
    let transContent = langOption[1].value;

    TranslateManager.add_queue(fromContent,transContent,content);
})

fromVoice.addEventListener("click", function () {
    let fromTalk;
    fromTalk = new SpeechSynthesisUtterance(fromText.value);
    fromTalk.lang = langOption[0].value;
    speechSynthesis.speak(fromTalk);
})

toVoice.addEventListener("click", function () {
    let fromTalk;
    fromTalk = new SpeechSynthesisUtterance(transText.value);
    fromTalk.lang = langOption[0].value;
    speechSynthesis.speak(fromTalk);
})

cpyBtn.addEventListener("click", function () {
    navigator.clipboard.writeText(transText.value);
})

fromText.addEventListener("keyup", function () {
    countValue.innerHTML = `${fromText.value.length}/5,000`;
})

exchangeLang.addEventListener("click", function () {
    let tempText = fromText.value;
    fromText.value = transText.value;
    transText.value = tempText;

    let tempOpt = langOption[0].value;
    langOption[0].value = langOption[1].value;
    langOption[1].value = tempOpt;
})

historyButton.addEventListener("click", function () {
    allContainer.classList.add("display-flex");
    historyBox.classList.add("show");
    fetch('/utility/history', {
        method: "POST",
        body: JSON.stringify({
            "from_item" : 0,
            "amount" : 1000
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            console.log('ERR');
        }
    })
    .then(data => {
        for (let key in data) {
            let ele = data[key];
            historyList.insertAdjacentHTML('afterbegin', displayHistoryEx(ele['from_language'],ele['to_language'],ele['from_content'],ele['to_content']));
        }
    })


})
function displayHistoryEx(from_lang,to_lang,from_text, to_text) {
    let htmls = "";
    htmls += `
        <div class="trans-item">
            <div class="lang-to-lang">${from_lang} 
                <span class="arrow"><ion-icon name="arrow-forward-outline"></ion-icon></span> ${to_lang} 
            </div>
            <div class="original-text">${from_text}</div>
            <div class="trans-text">${to_text}</div>
        </div>
    `;
    return htmls;
}

removeHistoryBox.addEventListener("click", function () {
    allContainer.classList.remove("display-flex");
    historyBox.classList.remove("show");
})

function displayHistory(fromText, transText) {
    let htmls = "";
    htmls += `
        <div class="trans-item">
            <div class="lang-to-lang">${language[langOption[0].value]} 
                <span class="arrow"><ion-icon name="arrow-forward-outline"></ion-icon></span> ${language[langOption[1].value]} 
            </div>
            <div class="original-text">${fromText}</div>
            <div class="trans-text">${transText}</div>
        </div>
    `;
    return htmls;
}
