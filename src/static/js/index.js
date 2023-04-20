console.log("Hello from index.js");
'use strict';

document.getElementById('menu-icon').addEventListener('click', toggleNav);

function toggleNav()
{
    if(document.querySelector('.dashboard-page-menu').style.width == "0px")
    {
        return openNav();
    }
    closearNav();
}

function openNav() 
{
    document.querySelector(".dashboard-page-menu").style.width = "300px";
}

function closearNav() 
{
    document.querySelector(".dashboard-page-menu").style.width = "0";
}


/*
    ADD USER FUNCTIONALITY
*/

const exampleModal = document.getElementById('exampleModal')
if (exampleModal) {
    // function getFields {
    //     const fields = document.querySelectorAll('.modal-body input')
    //     console.log(fields)
        
    // }
//   exampleModal.addEventListener('show.bs.modal', event => {
//     // Button that triggered the modal
//     const button = event.relatedTarget
//     // Extract info from data-bs-* attributes
//     // const recipient = button.getAttribute('data-bs-whatever')
//     // If necessary, you could initiate an Ajax request here
//     // and then do the updating in a callback.

//     // Update the modal's content.
//     // const modalTitle = exampleModal.querySelector('.modal-title')
//     // const modalBodyInput = exampleModal.querySelector('.modal-body input')

//     // modalTitle.textContent = `New message to ${recipient}`
//     // modalBodyInput.value = recipient
//   })
}
// const getFieldsValues = () =>({
//     name: document.querySelector('#floatingInput').value,
//     password: document.querySelector('#floatingPassword').value,
//     confirmPassword: document.querySelector('#floatingConfirmPassword').value,
//     role: parseInt(document.querySelector('#floatingRole').value)
// })

// document.querySelector('.register').addEventListener('click', function(e){
//     console.log('print something')
//     console.log (getFieldsValues())
// })