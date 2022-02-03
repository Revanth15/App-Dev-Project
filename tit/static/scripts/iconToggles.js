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

