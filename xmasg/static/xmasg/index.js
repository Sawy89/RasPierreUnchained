document.addEventListener('DOMContentLoaded', () => {

    // Set Sidebar visible element
    document.querySelectorAll('.sidebar-room-message').forEach(element => {
        element.style.display = "none";
    });
    document.querySelectorAll('.sidebar-room-other').forEach(element => {
        element.style.display = "none";
    });

});

