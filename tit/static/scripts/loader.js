var myModal = new bootstrap.Modal(document.getElementById('loader'), {
    keyboard: false
})
$(document).ready(function() {
    $('.tab-pane').not('.show.active').addClass('show active') 
    myModal.toggle()
    console.log('open!')
}) 

