document.addEventListener('DOMContentLoaded', () => {

    // Blurr
    divToCopy = document.querySelector(".content-text");
    divToChange = document.querySelector(".content-blur");
    divToChange.setAttribute("style","width:"+divToCopy.offsetWidth+"px");
    divToChange.setAttribute("style","heigth:"+divToCopy.offsetHeight+"px");

    // Set Sidebar Name
    roomName = document.querySelector('#room-name');
    if (roomName.innerHTML == '')
        roomName.innerHTML = 'XmasG'

});