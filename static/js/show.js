import { checkId, checkName } from './check.js';

export function checkBeforeQuery() {
    let name = document.getElementById('name').value;
    let id = document.getElementById('id').value;
    if (name == "" || id == "") {
        alert("请输入完整的查询条件");
        return;
    }
    if (!checkName(name)) {
        alert("姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文的字符串");
        return;
    }
    if (!checkId(id)) {
        alert("学号不合法，应当为一个长度为 1-16 的正整数");
        return;
    }
    document.getElementById('queryForm').submit();
}