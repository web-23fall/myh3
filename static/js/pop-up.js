let popup1 = document.querySelector(".popup1");
let popup2 = document.querySelector(".popup2");
let popup3 = document.querySelector(".popup3");

export function frontEndWarn(message) {
    let par = document.querySelector(".popup1 p");
    par.textContent = message;
    popup1.classList.toggle("popupActive");
}

export function backEndWarn(message) {
    let par = document.querySelector(".popup2 p");
    par.textContent = message;
    popup2.classList.toggle("popupActive");
}

export function success(message) {
    let par = document.querySelector(".popup3 p");
    par.textContent = message;
    popup3.classList.toggle("popupActive");
}

export function flashBackMessages() {
    let flashMessages = document.getElementById("flash-messages").children;
    console.assert(flashMessages.length <= 1);
    if(flashMessages.length != 0) {
        for(let i = 0;i < flashMessages.length;i++) {
            backEndWarn(flashMessages[i].textContent);
        }
    }
}

export function close1() {
    popup1.classList.toggle("popupActive");
    window.location.reload();
}

export function close2() {
    popup2.classList.toggle("popupActive");
    if(window.location.search) {
        window.location.replace(window.location.origin);
        return;
    }
    window.location.reload();
}

export function close3() {
    popup3.classList.toggle("popupActive");
    window.location.reload();
}

window.frontEndWarn = frontEndWarn;
window.backEndWarn = backEndWarn;
window.success = success;
window.close1 = close1;
window.close2 = close2;
window.close3 = close3;
