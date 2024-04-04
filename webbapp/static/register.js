function checkBothPasswords(passwordOne,passwordTwo){
    if (passwordOne === passwordTwo){
        return true
    }else{
        return false
    }
}


function ableDisableButton(){
    var passwordOne = document.getElementById("password").value
    var passwordTwo = document.getElementById("passwordrepeat").value
    var message = document.getElementById("message_passwords")
    var button = document.getElementById("button_register")

    if (checkBothPasswords(passwordOne,passwordTwo)){
        button.disabled = false
        message.innerHTML = "" 
    }else{
        button.disabled = true
        message.innerHTML = "Both passwords should match"
    }
}