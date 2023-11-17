import {flashBackMessages} from "./pop-up.js";
import {
    checkAge,
    checkHometown,
    checkId,
    checkName,
    frontEndWarnAge,
    frontEndWarnHometown,
    frontEndWarnId,
    frontEndWarnName
} from "./check.js";

export function checkAndSubmit() {
    const id = document.getElementById('stu_id').value;
    const name = document.getElementById('stu_name').value;
    const age = document.getElementById('stu_age').value;
    const hometown = document.getElementById('stu_origin').value;
    const male = document.getElementById('male').checked;
    const female = document.getElementById('female').checked;
    const form = document.getElementById('insertForm');
    if (!checkId(id)) {
        frontEndWarnId();
        return;
    }
    if (!checkName(name)) {
        frontEndWarnName();
        return;
    }
    if (male === false && female === false) {
        frontEndWarn('请选择性别');
        return;
    }
    if (!checkAge(age)) {
        frontEndWarnAge();
        return;
    }
    if (!checkHometown(hometown)) {
        frontEndWarnHometown();
        return;
    }
    form.submit();
}

window.onload = flashBackMessages;
window.checkAndSubmit = checkAndSubmit;