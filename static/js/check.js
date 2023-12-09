import {frontEndWarn} from './pop-up.js';

const checkSQLkeyword = (str) => {
    const regex = /\b(?:and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|declare|or)\b/g;
    return regex.test(str);
}

const checkStringWithUpperLowerChineseSpace = (str) => {
    // contains [A-Z], [a-z], chinese characters, space
    // not contains [0-9], [!@#$%^&*-_,]
    let typeUpper = 0;
    let typeLower = 0;
    let typeChinese = 0;
    let typeSpace = 0;
    for(let char of str) {
        if(char >= 'A' && char <= 'Z') {
            typeUpper = 1;
        }
        if(char >= 'a' && char <= 'z') {
            typeLower = 1;
        }
        if(char >= '\u4e00' && char <= '\u9fa5') {
            typeChinese = 1;
        }
        if(char === ' ') {
            typeSpace = 1;
        }
        if(char === ',' || char === '!' || char === '@' || char === '#' || char === '$' || char === '%' || char === '^' || char === '&' || char === '*' || char === '-' || char === '_') {
            return false;
        }
        if(char >= '0' && char <= '9') {
            return false;
        }
    }
    if (typeSpace) {
        return (typeUpper + typeLower + typeChinese) >= 1;
    }
    return (typeUpper + typeLower + typeChinese + typeSpace) >= 1;
}

const checkStringWithUpperLowerNumSpecialAtLeastThreeTypes = (str) => {
    // contains [A-Z], [a-z], [0-9], [!@#$%^&*-_] at least three types
    let typeUpper = 0;
    let typeLower = 0;
    let typeNum = 0;
    let typeSpecial = 0;
    for(let char of str) {
        if(char >= 'A' && char <= 'Z') {
            typeUpper = 1;
        }
        if(char >= 'a' && char <= 'z') {
            typeLower = 1;
        }
        if(char >= '0' && char <= '9') {
            typeNum = 1;
        }
        if(char === '!' || char === '@' || char === '#' || char === '$' || char === '%' || char === '^' || char === '&' || char === '*' || char === '-' || char === '_') {
            typeSpecial = 1;
        }
    }
    return (typeUpper + typeLower + typeNum + typeSpecial) >= 3;
}

const checkStringWithSpecificLength = (str, min, max) => {
    // check len >= min && <= max
    return str.length >= min && str.length <= max;
}

const checkWhiteChar = (str) => {
    // check white char
    const regex = /\s/g;
    return regex.test(str);

}

export const checkUsername = (username) => {
    if(checkWhiteChar(username)) {
        return false;
    }
    // check username
    if(checkSQLkeyword(username)) {
        return false;
    }
    // len >= 6 && <= 16, contains [A-Z], [a-z], [0-9], [!@#$%^&-_] at least three types, start with [A-Za-z0-9_]
    if (!checkStringWithSpecificLength(username, 6, 16)) {
        return false;
    }
    const firstLetterRegex = /^[A-Za-z0-9_]/;
    if (!firstLetterRegex.test(username[0])) {
        return false;
    }
    return checkStringWithUpperLowerNumSpecialAtLeastThreeTypes(username);
}

export const checkPassword = (password) => {
    // check password by regex or other ways
    if(checkWhiteChar(password)) {
        return false;
    }
    if(checkSQLkeyword(password)) {
        return false;
    }
    // len >= 6 && <= 16, contains [A-Z], [a-z], [0-9], [!@#$%^&-_] at least three types
    return checkStringWithUpperLowerNumSpecialAtLeastThreeTypes(password) &&
        checkStringWithSpecificLength(password, 6, 16);
}

// TODO: debug
export const checkName = (name) => {
    //check name
    if(checkSQLkeyword(name)) {
        return false;
    }
    // len >= 1 && <= 16, contains [A-Za-z], chinese characters, space
    return checkStringWithUpperLowerChineseSpace(name) &&
        checkStringWithSpecificLength(name, 1, 16);
}

export const checkId = (id) => {
    // check id by regex
    // len <= 16, contains [0-9], positive integer
    let regex = /^[1-9][0-9]{0,15}$/;
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
    if(checkSQLkeyword(hometown)) {
        return false;
    }
    // len >= 1 && <= 16, contains [A-Za-z], chinese characters, space
    return checkStringWithUpperLowerChineseSpace(hometown) &&
        checkStringWithSpecificLength(hometown, 1, 16);
}

export const frontEndWarnUsername = () => {
    frontEndWarn("用户名不合法，应当为一个长度为 6-16 的，以大小写字母或数字或下划线开头的，包含大小写字母、数字和特殊字符的其中三种的字符串，且不包含任何 SQL 关键字");
}

export const frontEndWarnPassword = () => {
    frontEndWarn("密码不合法，应当为一个长度为 6-16 的，同时具有大写、小写、数字、特殊字符其中三种的字符串，且不包含任何 SQL 关键字");
}

export const frontEndWarnName = () => {
    frontEndWarn("姓名不合法，应当为一个长度为 1-16 的，可包含空格，中文，英文，但不包含数字和特殊字符的字符串，且不包含任何 SQL 关键字");
}

export const frontEndWarnId = () => {
    frontEndWarn("学号不合法，应为一个长度为 1-16 的正整数");
}

export const frontEndWarnAge = () => {
    frontEndWarn("年龄不合法，应当为一个 1-100 的正整数");
}

export const frontEndWarnHometown = () => {
    frontEndWarn("籍贯不合法，应当为一个长度为 1-16 的，包含中英文的字符串，且不包含任何 SQL 关键字");
}