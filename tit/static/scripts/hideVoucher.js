// function myFunction() {
//     var x = document.getElementById("myDIV");
//     if (x.style.display === "none") {
//       x.style.display = "block";
//     } else {
//       x.style.display = "none";
//     }
//   }



// function myFunction() {
//     var x = $(this).parent('div').prev().prev().prev().prev().find('.vouchers').text();
//     console.log(x);
//     if (x.style.display === "none") {
//       x.style.display = "block";
//     } else {
//       x.style.display = "none";
//     }
//   }


  
//   $('.hide').click( function() {
//     var copyText = $(this).parent('div').prev().find('.vcode').text().split(': ')[1]
//     var $temp = $("<input>");
//     $("body").append($temp);
//     $temp.val(copyText).select();
//     $temp.select()
//     document.execCommand("copy");
//     $temp.remove()
//   }) 
  
// function myFunction() {
//     document.getElementsByClassName("vouchers").style.display = "none";
//     }

// $('.hide').click.style.display = "none";




// $('.hide').click( function() {
//     var hide = $(this).parent('div').prev().prev().prev().prev().find('.vouchers').text()
//     hide.style.display = 'none'
//   }) 



$(document).ready(function(){
  $("#hide").click(function(){
    $("p").hide();
    $("img").hide();
  });
  $("#show").click(function(){
    $("p").show();
    $("img").show();
  });
});



