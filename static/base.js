document.addEventListener('DOMContentLoaded', () => {

    // Sidebar management
    elSidebar = document.querySelector('#sidebarCollapse');
    if (elSidebar != "undefined"  &&  elSidebar != null)
        elSidebar.addEventListener('click', function() {
            document.querySelector('#sidebar').classList.toggle('active');
            document.querySelector('#sidebarCollapse').classList.toggle('active');
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
}