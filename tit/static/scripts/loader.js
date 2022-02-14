var myModal = new bootstrap.Modal(document.getElementById('loader'), {
    keyboard: false
})
$(document).ready(function() {
    $('.tab-pane').not('.show.active').addClass('show active') 
    myModal.toggle()
    console.log('open!')
}) 

function hidetabs() {
    id = $('.nav-link.active').attr('data-bs-target')
    $('.tab-pane').not(id).removeClass('show active')
    myModal.hide()
    console.log('close!')
}
