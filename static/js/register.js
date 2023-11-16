import { checkUsername, checkPassword } from './check.js'

export function checkBeforeRegister() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('pwd').value;
    let passwordAgain = document.getElementById('pwdagain').value;
    if(username == "" || password == "") {
        alert("用户名或密码不能为空");
        return;
    }
    if(passwordAgain == "") {
        alert("请确认密码");
        return;
    }
    if(username == password) {
        alert("用户名和密码不能相同");
        return;
    }
    if(password != passwordAgain) {
        alert("两次输入的密码不一致");
        return;
    }
    if (!checkUsername(username)) {
        alert("用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串");
        return;
    }
    if (!checkPassword(password)) {
        alert("密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串");
        return;
    }
    document.getElementById('registerForm').submit();
}

window.checkBeforeRegister = checkBeforeRegister;