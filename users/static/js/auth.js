var button = document.getElementById("btn");
var register_form = document.getElementById("register-form");
var login_form = document.getElementById("login-form");

function register(){
    button.style.left= "110px";
    register_form.hidden = false;
    login_form.hidden = true;
}
function login(){
    button.style.left = "0px";
    register_form.hidden = true;
    login_form.hidden = false
}
console.log(is_register);
if (is_register){register();}