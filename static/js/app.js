let footerDate = document.querySelector("#footer-date")
let date = new Date
footerDate.innerText = date.getFullYear()

try {
    let searchToggleEl = document.querySelector('#search_toggle')
    let modalEl = document.getElementById('nav-menu')
    searchToggleEl.addEventListener('click', ()=>{
        modalEl.classList.remove('d-md-none')
        document.querySelector('#q').focus()
    })
} catch (TypeError) {

}