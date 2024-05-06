/**
 * Check that both passwords are equal
 * @param {string} passwordOne 
 * @param {string} passwordTwo 
 * @returns {boolean}
 */
function checkBothPasswords(passwordOne,passwordTwo){
    if (passwordOne === passwordTwo){
        return true
    }else{
        return false
    }
}

/**
 * Check that the variables are not empty
 * @param {string} passwordOne 
 * @param {string} passwordTwo 
 * @param {string} username 
 * @param {string} email 
 * @param {string} name 
 * @param {string} surname 
 * @returns {boolean}
 */
function notEmptyVars(passwordOne,passwordTwo,username,email,name,surname){

    var passwordOneCheck = passwordOne.trim()
    var passwordTwoCheck = passwordTwo.trim()
    var usernameCheck = username.trim()
    var emailCheck = email.trim()
    var nameCheck = name.trim()
    var surnameCheck = surname.trim()

    if (passwordOneCheck === '' || 
        passwordTwoCheck === '' || 
        usernameCheck === '' || 
        emailCheck === '' || 
        nameCheck === '' || 
        surnameCheck === '') {
        return false;
    } else {
        return true;
    }
}

/**
 * This function disable the button if there is something incorrect and enables it if everything is ok
 */
function ableDisableButton(){

    // get variables from form
    var passwordOne = document.getElementById("password").value
    var passwordTwo = document.getElementById("passwordrepeat").value
    var username = document.getElementById("username").value
    var email = document.getElementById("email").value
    var name = document.getElementById("name").value
    var surname = document.getElementById("surname").value

    // messages and button
    var message = document.getElementById("message_passwords")
    var button = document.getElementById("button_register")

    // checks
    var notEmptyVarsCheck = notEmptyVars(passwordOne,passwordTwo,username,email,name,surname)
    var bothPasswordsEqual = checkBothPasswords(passwordOne,passwordTwo)

    if (notEmptyVarsCheck){
        if (bothPasswordsEqual){
            button.disabled = false
            message.innerHTML = "" 
        }else{
            button.disabled = true
            message.innerHTML = "Both passwords should match."
        }
    }else{
        button.disabled = true
        message.innerHTML = "All fields should be filled."
    }

}