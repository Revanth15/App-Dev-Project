function toggleNav() {
    let navText = document.querySelectorAll(".navText")
    navText.forEach(text => {
      text.classList.toggle("d-none")
    });
    //document.getElementById("sideNav").classList.toggle("transition")
  }