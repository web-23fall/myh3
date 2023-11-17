import { checkUsername, checkPassword, frontEndWarnUsername, frontEndWarnPassword } from './check.js';
import { frontEndWarn, backEndWarn, flashBackMessages } from './pop-up.js';

let lastImagePath = "";
let code = "";
function requestForCode() {
    $.ajax({
        url: '/code',
        type: 'POST',
        data: {
            request_code: true,
            last_image_path: lastImagePath
        },
        dataType: 'json',
        async: false,
        success: function(response) {
            if (response.code.toString() == "server_error") {
                backEndWarn("服务器意外错误，请刷新页面重试");
            } else if (response.code.toString() != "error") {
                code = response.code.toString();
                lastImagePath = response.path.toString();
            }
            return;
        },
        error: function(error) {
            backEndWarn(error);
        }
    });
    return code;
}

export function send() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('pwd').value;
    if(username == "" || password == "") {
        frontEndWarn("用户名或密码不能为空");
        return;
    }
    if(username == password) {
        frontEndWarn("用户名和密码不能相同");
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
    code = requestForCode();
    $("#code-modal").modal("show");
    document.getElementById("code-content").innerHTML = "<img src='.." + lastImagePath.substring(1) + "'/>";
}

export function again() {
    code = requestForCode();
    document.getElementById("code-content").innerHTML = "<img src='.." + lastImagePath.substring(1) + "'/>";
}

window.onload = flashBackMessages;

window.send = send;
window.again = again;