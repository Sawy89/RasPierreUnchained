// document.querySelector('#room-name-input').focus();
// document.querySelector('#room-name-input').onkeyup = function(e) {
//     if (e.keyCode === 13) {  // enter, return
//         document.querySelector('#room-name-submit').click();
//     }
// };

// document.querySelector('#room-name-submit').onclick = function(e) {
//     var roomName = document.querySelector('#room-name-input').value;
//     window.location.pathname = '/chat/' + roomName + '/';
// };



document.addEventListener('DOMContentLoaded', () => {

    // Set Sidebar visible element
    
    // // New Room clicked
    // disableButton(document.querySelector('#new-room'), document.querySelector('input[name="new-room"]'));
    // document.querySelector('#new-room').onclick = function () {
    //     newRoomClicked();
    // };

    // // New room added
    // socket.on('new room', data => {
    //     dispNewRoom(data);
    // });

});



// // FUNCTION: DISABLE-ENABLE button on TEXT
// function disableButton(buttonE, textE) {
//     // By default, submit button is disabled
//     buttonE.disabled = true;

//     // Enable button only if there is text in the input field
//     textE.onkeyup = () => {
//         if (textE.value.length > 0)
//             buttonE.disabled = false;
//         else
//             buttonE.disabled = true;
//     };
// };


// // Function new 