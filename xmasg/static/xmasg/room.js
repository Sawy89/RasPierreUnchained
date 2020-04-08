document.addEventListener('DOMContentLoaded', () => {

    // Set Sidebar Name
    roomName = document.querySelector('#room-name');
    if (roomName.innerHTML == '')
        roomName.innerHTML = 'XmasG'

    // Disable admin checkbox if not admin
    if (roomAdmin == true) {
        document.querySelectorAll('input[name="is-admin"]').forEach(element => {
            element.disabled = true;
        });
    };

});
