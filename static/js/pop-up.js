// if (从后端发送的信息存在，记为message)
let blue = document.querySelector("#container");
let popup1 = document.querySelector(".popup1");
let popup2 = document.querySelector(".popup2");
let popup3 = document.querySelector(".popup3");
blue.classList.toggle("active");
if (message === 'success')
    popup3.classList.toggle("popupActive");
else
    popup2.classList.toggle("popupActive");

function toggle() {
    let blue = document.querySelector("#container");
    let popup1 = document.querySelector(".popup1");
    let popup2 = document.querySelector(".popup2");
    let popup3 = document.querySelector(".popup3");

    //  if (message 不存在)
    let flag_front = true;

    // 前端验证

    if (!flag_front) {
        blue.classList.toggle("active");
        popup1.classList.toggle("popupActive");
    }
    else {
        document.getElementById('deleteForm').submit();
    }
}
