import {flashBackMessages} from "./pop-up.js";
import {
    checkAge,
    checkHometown,
    checkId,
    checkName,
    frontEndWarnAge,
    frontEndWarnHometown,
    frontEndWarnName
} from "./check.js";

export function checkBeforeUpdate() {
    const name = document.getElementById('stu_name').value;
    const age = document.getElementById('stu_age').value;
    const hometown = document.getElementById('stu_origin').value;
    const male = document.getElementById('male').checked;
    const female = document.getElementById('female').checked;
    const form = document.getElementById('updateForm');
    if(!checkName(name)) {
        frontEndWarnName();
        return;
    }
    if(male === false && female === false) {
        frontEndWarn('请选择性别');
        return;
    }
    if(!checkAge(age)) {
        frontEndWarnAge();
        return;
    }
    if(!checkHometown(hometown)) {
        frontEndWarnHometown();
        return;
    }
    form.submit();
}

window.onload = flashBackMessages;
window.checkBeforeUpdate = checkBeforeUpdate;