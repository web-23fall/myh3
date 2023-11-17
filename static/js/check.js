import { frontEndWarn, backEndWarn } from './pop-up.js';
const checkStringWithUpperLowerChineseSpace = (str) => {
    // contains [A-Z], [a-z], chinese characters, space
    const typeUpper = ((str.match(/[A-Z]/g) || []).length) > 0;
    const typeLower = ((str.match(/[a-z]/g) || []).length) > 0;
    const typeChinese = ((str.match(/[\u4e00-\u9fa5]/g) || []).length) > 0;
    const typeSpace = ((str.match(/ /g) || []).length) > 0;
    if(typeSpace) {
        return (typeUpper + typeLower + typeChinese) >= 1;
    }
    return (typeUpper + typeLower + typeChinese + typeSpace) >= 1;
}

const checkStringWithUpperLowerNumSpecialAtLeastThreeTypes = (str) => {
    // contains [A-Z], [a-z], [0-9], [!@#$%^&*-_] at least three types
    const typeUpper = ((str.match(/[A-Z]/g) || []).length) > 0;
    const typeLower = ((str.match(/[a-z]/g) || []).length) > 0;
    const typeNum = ((str.match(/[0-9]/g) || []).length) > 0;
    const typeSpecial = ((str.match(/[!@#$%^&-_]/g) || []).length) > 0;
    return (typeUpper + typeLower + typeNum + typeSpecial) >= 3;
}

const checkStringWithSpecificLength = (str, min, max) => {
    // check len >= min && <= max
    return str.length >= min && str.length <= max;
}

export const checkUsername = (username) => {
    // check username
    // len >= 6 && <= 16, contains [A-Z], [a-z], [0-9], [!@#$%^&-_] at least three types, start with [A-Za-z0-9_]
    if(!checkStringWithSpecificLength(username, 6, 16)) {
        return false;
    }
    const firstLetterRegex = /^[A-Za-z0-9_]/;
    if(!firstLetterRegex.test(username[0])) {
        return false;
    }
    return checkStringWithUpperLowerNumSpecialAtLeastThreeTypes(username);
}

export const checkPassword = (password) => {
    // check password by regex or other ways
    // len >= 6 && <= 16, contains [A-Z], [a-z], [0-9], [!@#$%^&-_] at least three types
    return checkStringWithUpperLowerNumSpecialAtLeastThreeTypes(password) && 
           checkStringWithSpecificLength(password, 6, 16);
}

export const checkName = (name) => {
    //check name
    // len >= 1 && <= 16, contains [A-Za-z], chinese characters, space
    return checkStringWithUpperLowerChineseSpace(name) && 
           checkStringWithSpecificLength(name, 1, 16);
}

export const checkId = (id) => {
    // check id by regex
    // len <= 16, contains [0-9]
    let regex = /^[0-9]{1,16}$/;
    return regex.test(id);
}

export const checkAge = (age) => {
    // check age by regex
    // age >= 1 && <= 100 positive integer
    const regex = /^(?:[1-9]|[1-9]\d|100)$/;
    return regex.test(age);
}

export const checkHometown = (hometown) => {
    // check hometown
    // len >= 1 && <= 16, contains [A-Za-z], chinese characters, space
    return checkStringWithUpperLowerChineseSpace(hometown) && 
           checkStringWithSpecificLength(hometown, 1, 16);
}

export const frontEndWarnUsername = () => {
    frontEndWarn("用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串");
}

export const frontEndWarnPassword = () => {
    frontEndWarn("密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串");
}

export const frontEndWarnName = () => {
    frontEndWarn("姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串");
}

export const frontEndWarnId = () => {
    frontEndWarn("学号不合法，应为一个长度为 1-16 的正整数");
}

export const frontEndWarnAge = () => {
    frontEndWarn("年龄不合法，应当为一个 1-100 的正整数");
}

export const frontEndWarnHometown = () => {
    frontEndWarn("籍贯不合法，应当为一个长度为 1-16 的，包含中英文的字符串");
}