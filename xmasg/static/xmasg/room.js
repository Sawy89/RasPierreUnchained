document.addEventListener('DOMContentLoaded', () => {

    // Set Sidebar Name
    roomName = document.querySelector('#room-name');
    if (roomName.innerHTML == '')
        roomName.innerHTML = 'XmasG'

    // Disable admin checkbox if not admin
    if (roomAdmin == false) {
        document.querySelectorAll('input[name="is-admin"]').forEach(element => {
            element.disabled = true;
        });
    };

    // Disable exclusion checkbox if not member
    if (userIsMember == false) {
        document.querySelectorAll('input[name="is-your-exclusion"]').forEach(element => {
            element.disabled = true;
        });
    };

    // Button modify members
    document.querySelector('#bnt-change-member').disabled = true;
    document.querySelectorAll('.room-member input').forEach(element => {
        element.addEventListener("change", checkInputChange, false);
    });

    // Submit change on RoomMember
    document.querySelector('#bnt-change-member').onclick = function () {
        // Admin change
        if (roomAdmin == true) {
            document.querySelectorAll('input[name="is-admin"]').forEach(element => {
                if (isEqualToDefault(element) == false) {
                    roommemberModification(element);
                }
            });
        };
        // Exclusion change
        if (userIsMember == true) {
            document.querySelectorAll('input[name="is-your-exclusion"]').forEach(element => {
                if (isEqualToDefault(element) == false) {
                    roommemberModification(element);
                }
            });
        };

        // Reload page
        setTimeout('', 5000); // ToDo: improve by waiting for answer!
        location.reload();
    };

    // Set countDown
    if (document.querySelectorAll('.li-countdown').length > 0)
        setCountdown();

});


// If Input change from default, disable button
function checkInputChange() {
    buttonChange = document.querySelector('#bnt-change-member');
    if (isEqualToDefault(this)) {
        // if one is equal --> CHECK ALL to be sure!
        buttonChange.disabled = true; // init = disable
        document.querySelectorAll('.room-member input').forEach(element => {
            if (isEqualToDefault(element) == false) {buttonChange.disabled = false;} // if one is different, enable
        });
    }
    else {
        // if one is different, enabled
        buttonChange.disabled = false;
    }
};


function isEqualToDefault(element) {
    // Convert current status: "checked" or empty
    if (element.checked) {var currentStatus = 'checked'}
    else {var currentStatus = ''}
    // Check if it's the same
    if (element.dataset.defaultvalue == currentStatus) {return true;}
    else {return false;}
};


// AJAX modification sent
function roommemberModification(element) {
    // Create POST request
    var csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', url_xmasgajax_roommember_modification);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrftoken)  // add csrf token for Django!
    
    // Result of request
    request.onload = () => {
        // const data = JSON.parse(request.responseText);
        if (request.status == 200) 
            return true;
        else
            alert('Something went wrong! Try again!')
    };

    // Send
    var elName = element.name;
    var elMemberId = parseInt(element.id.split('-')[1]);
    var elChecked = element.checked;
    var messageJson = {'roomId': room_id, 'elName': elName, 'elMemberId': elMemberId, 'elChecked': elChecked};
    request.send(JSON.stringify(messageJson));
}


// Countdown https://codepen.io/AllThingsSmitty/pen/JJavZN
function setCountdown() {

const second = 1000,
      minute = second * 60,
      hour = minute * 60,
      day = hour * 24;

let countDown = new Date(room_end_date).getTime(),
    x = setInterval(function() {    

      let now = new Date().getTime(),
          distance = countDown - now;

      document.getElementById('days').innerText = Math.floor(distance / (day)),
        document.getElementById('hours').innerText = Math.floor((distance % (day)) / (hour)),
        document.getElementById('minutes').innerText = Math.floor((distance % (hour)) / (minute)),
        document.getElementById('seconds').innerText = Math.floor((distance % (minute)) / second);

      //do something later when date is reached
      if (distance < 0) {
       // Reload page
       setTimeout('', 5000);
       location.reload();
      };

    }, second)
};