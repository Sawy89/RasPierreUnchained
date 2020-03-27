document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#sidebarCollapse').addEventListener('click', function() {
        document.querySelector('#sidebar').classList.toggle('active');
        document.querySelector('#sidebarCollapse').classList.toggle('active');
    });

});