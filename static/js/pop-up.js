// if (从后端发送的信息存在，记为message)
let popup1 = document.querySelector(".popup1");
let popup2 = document.querySelector(".popup2");
let popup3 = document.querySelector(".popup3");
// if (message === 'success')
//     popup3.classList.toggle("popupActive");
// else
//     popup2.classList.toggle("popupActive");

// function toggle() {
//     let blue = document.querySelector("#container");
//     let popup1 = document.querySelector(".popup1");
//     let popup2 = document.querySelector(".popup2");
//     let popup3 = document.querySelector(".popup3");

//     //  if (message 不存在)
//     let flag_front = true;

//     // 前端验证

//     if (!flag_front) {
//         blue.classList.toggle("active");
//         popup1.classList.toggle("popupActive");
//     }
//     else {
//         document.getElementById('deleteForm').submit();
//     }
// }

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

export function close1() {
    popup1.classList.toggle("popupActive");
}

export function close2() {
    popup2.classList.toggle("popupActive");
}

export function close3() {
    popup3.classList.toggle("popupActive");
}

window.frontEndWarn = frontEndWarn;
window.backEndWarn = backEndWarn;
window.success = success;
window.close1 = close1;
window.close2 = close2;
window.close3 = close3;
