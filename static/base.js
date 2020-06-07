document.addEventListener('DOMContentLoaded', () => {

    // Sidebar management
    elSidebar = document.querySelector('#sidebarCollapse');
    if (elSidebar != "undefined"  &&  elSidebar != null)
        elSidebar.addEventListener('click', function() {
            document.querySelector('#sidebar').classList.toggle('active');
            document.querySelector('#sidebarCollapse').classList.toggle('active');
            document.querySelector('#content').classList.toggle('not-active');
        });
    
        if (window.innerWidth < 480) {
            document.querySelector('#sidebar').classList.add('active');
            document.querySelector('#sidebarCollapse').classList.add('active');
            document.querySelector('#content').classList.remove('not-active');
        }
    
    // Blurr
    blurrHeigth();
    document.addEventListener("change", function(event) {
        blurrHeigth();
    });

});


// Get DJANGO cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


// blurr adapt heigth
function blurrHeigth() {
    divToCopy = document.querySelector(".content-text");
    divToChange = document.querySelector(".content-blur");
    if (divToCopy!=null && divToChange!=null) {
        divToChange.setAttribute("style","width:"+divToCopy.offsetWidth+"px");
        divToChange.setAttribute("style","height:"+divToCopy.offsetHeight+"px");
    };
};