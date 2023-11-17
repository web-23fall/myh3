import {flashBackMessages, frontEndWarn} from "./pop-up.js";
import {checkAge, frontEndWarnAge} from "./check.js";

export function checkBeforeUpdateAge() {
    let age = document.getElementById('age').value;
    let form = document.getElementById('updateAge');
    let checkboxes = form.querySelectorAll('input[type="checkbox"]');
    let cnt = 0;
    checkboxes.forEach(function(checkbox) {
        if(checkbox.checked) {
            cnt++;
        }
    });
    if(cnt === 0) {
        frontEndWarn("请至少选中一项，否则无法修改");
        return;
    }
    if(!checkAge(age)) {
        frontEndWarnAge();
        return;
    }
    form.submit();
}

window.onload = flashBackMessages;
window.checkBeforeUpdateAge = checkBeforeUpdateAge;