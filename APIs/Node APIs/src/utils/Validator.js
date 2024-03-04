module.exports.validateEmail = function(email) {
    const emailValidatorRegex = /^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/
    if (email.match(emailValidatorRegex)) return true;
    else return false;
}

module.exports.validateName = function(name) {
    const nameValidatorRegex = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/; 
    if (name.match(nameValidatorRegex)) return false; //The above chars should not be present.
    else return true;
}

module.exports.validatePassword = function(password) {
    const passwordValidatorRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (password.match(passwordValidatorRegex)) return true;
    else return false;
}