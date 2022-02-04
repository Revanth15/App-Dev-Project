$('#notificationdropdown').blur( function(){
    if ($(this).attr('class').includes('show')) {

      $(this).find('i').toggleClass('bi-bell')
      $(this).find('i').toggleClass('bi-bell-fill')
    }
})

$('#notificationdropdown').click( function(){

  $(this).find('i').toggleClass('bi-bell')
  $(this).find('i').toggleClass('bi-bell-fill')
  
})

$(document).ready(function(){
  if($('li span.p-1').length == 0) {
    $('span.p-1').remove()
  }
})
