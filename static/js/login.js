import { checkUsername, checkPassword } from './check.js';

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
                alert("服务器意外错误，请刷新页面重试");
            } else if (response.code.toString() != "error") {
                code = response.code.toString();
                lastImagePath = response.path.toString();
            }
            return;
        },
        error: function(error) {
            console.log(error);
        }
    });
    return code;
}

export function send() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('pwd').value;
    if(username == "" || password == "") {
        alert("用户名或密码不能为空");
        return;
    }
    if(username == password) {
        alert("用户名和密码不能相同");
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
    code = requestForCode();
    $("#code-modal").modal("show");
    document.getElementById("code-content").innerHTML = "<img src='.." + lastImagePath.substring(1) + "'/>";
}

export function again() {
    code = requestForCode();
    document.getElementById("code-content").innerHTML = "<img src='.." + lastImagePath.substring(1) + "'/>";
}

window.send = send;
window.again = again;