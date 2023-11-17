import { checkUsername, checkPassword, frontEndWarnUsername, frontEndWarnPassword } from './check.js';
import { frontEndWarn, backEndWarn, flashBackMessages } from './pop-up.js';

export function checkBeforeRegister() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('pwd').value;
    let passwordAgain = document.getElementById('pwdagain').value;
    if(username == "" || password == "") {
        frontEndWarn("用户名或密码不能为空");
        return;
    }
    if(passwordAgain == "") {
        frontEndWarn("请确认密码");
        return;
    }
    if(username == password) {
        frontEndWarn("用户名和密码不能相同");
        return;
    }
    if(password != passwordAgain) {
        frontEndWarn("两次输入的密码不一致");
        return;
    }
    if (!checkUsername(username)) {
        frontEndWarnUsername();
        return;
    }
    if (!checkPassword(password)) {
        frontEndWarnPassword();
        return;
    }
    document.getElementById('registerForm').submit();
}

window.checkBeforeRegister = checkBeforeRegister;
window.onload = flashBackMessages;