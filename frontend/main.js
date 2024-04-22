let langOption = document.querySelectorAll('select');
let fromText = document.querySelector(".fromText");
let transText = document.querySelector(".toTranslate");
let fromVoice = document.querySelector(".from");
let toVoice = document.querySelector(".to");
let cpyBtn = document.querySelector(".bx-copy");
let countValue = document.querySelector(".code_length");
let exchangeLang = document.querySelector(".bx-transfer");

const historyButton = document.querySelector(".history");
const historyBox = document.querySelector(".box-history");
const allContainer = document.querySelector(".all-container");
const boxContainer = document.querySelector(".box-container");

const removeHistoryBox = document.querySelector(".remove-sidebar");

const historyList = document.querySelector("#history-list");

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

    // let transLink = `https://api.mymemory.translated.net/get?q=${content}!&langpair=${fromContent}|${transContent}`;

    fetch('/translate/text', {
        method: "POST",
        body: JSON.stringify({
            "from_language": fromContent,
            "to_language": transContent,
            "content": content,
        })
    })
        .then(translate => translate.json())
        .then(data => {
            transText.value = data["text"];
            historyList.innerHTML += displayHistory(content, transText.value);
        })
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
})

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
