console.log("Hello from index.js");
'use strict';

document.getElementById('menu-icon').addEventListener('click', toggleNav);

function toggleNav() {
    if (document.querySelector('.dashboard-page-menu').style.width == "0px") {
        return openNav();
    }
    closearNav();
}

function openNav() {
    document.querySelector(".dashboard-page-menu").style.width = "300px";
}

function closearNav() {
    document.querySelector(".dashboard-page-menu").style.width = "0";
}

// TOOGLE FIELD PASSWORD

document.body.addEventListener('click', function (e) {    
    if (!e.target.classList.contains('eye-toggle-icon')) return;
    const inputPassword = e.target.previousElementSibling.children[0];
    if (inputPassword.type === 'password') inputPassword.type = 'text';
    else inputPassword.type = 'password';
})