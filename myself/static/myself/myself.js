document.addEventListener('DOMContentLoaded', () => {

    

});


// Show detail of the section selected
function showDetail(el_id) {
    // Check if other button clicked: if so, hide them
    Array.from(document.getElementsByClassName('content2-main')).forEach(element => {
        if (!(element.classList.contains('hidden')))
            hideDetail(element.dataset.id);
    });
    // Hide button
    document.getElementById(el_id+'-showButton').classList.toggle('hidden');
    // Show detail block and adjust blur
    document.getElementById(el_id+'-content2').classList.toggle('hidden');
    document.getElementById(el_id+'-content3').classList.toggle('hidden');
    document.getElementById(el_id+'-blur').style.height = document.getElementById(el_id+'-detail').offsetHeight+'px';

    // Position in the right place (next to "main")
    document.getElementById(el_id+'-blur').style.top = document.getElementById(el_id+'-content').offsetTop+'px';
    document.getElementById(el_id+'-detail').style.top = document.getElementById(el_id+'-content').offsetTop+'px';
}

function hideDetail(el_id) {
    // Show again detail button
    document.getElementById(el_id+'-showButton').classList.toggle('hidden');
    // Hide detail block and blur
    document.getElementById(el_id+'-content2').classList.toggle('hidden');
    document.getElementById(el_id+'-content3').classList.toggle('hidden');
    document.getElementById(el_id+'-blur').style.height = 'auto';
}   