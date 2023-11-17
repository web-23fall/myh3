import {checkId, checkName, frontEndWarnId, frontEndWarnName} from './check.js';
import {backEndWarn, flashBackMessages, frontEndWarn, success} from "./pop-up.js";

export function checkBeforeQuery() {
    let name = document.getElementById('name').value;
    let id = document.getElementById('id').value;
    if (name == "" || id == "") {
        frontEndWarn("请输入完整的查询条件");
        return;
    }
    if (!checkName(name)) {
        frontEndWarnName();
        return;
    }
    if (!checkId(id)) {
        frontEndWarnId();
        return;
    }
    document.getElementById('queryForm').submit();
}

function submit(idList) {
    console.log(idList);
    $.ajax({
        url: '/delete_all',
        type: 'POST',
        data: {
            ids: idList
        },
        dataType: 'json',
        async: false
    });
}

export function deleteForm() {
    let form = document.getElementById('deleteForm');
    let checkboxes = form.querySelectorAll('input[type="checkbox"]');
    let cnt = 0;
    let ids = [];
    checkboxes.forEach(function(checkbox) {
        if(checkbox.checked) {
            cnt++;
            ids.push(checkbox.value);
        }
    });
    if(cnt == 0) {
        frontEndWarn("请至少选中一项，否则无法删除");
        return;
    }
    // 不需要刷新页面，用 ajax 重写 submit 逻辑
    submit(ids);
    let flashMessages = document.getElementById("flash-messages").children;
    if(flashMessages.length == 0) {
        success('批量删除成功，点击下方确认后刷新页面');
        return;
    }
}

window.onload = flashBackMessages;
window.checkBeforeQuery = checkBeforeQuery;
window.deleteForm = deleteForm;