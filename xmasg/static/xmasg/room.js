document.addEventListener('DOMContentLoaded', () => {

    // Check extraction date
    if (room_end_date)
        var countDownInit = new Date(room_end_date).getTime();
    var nowInit = new Date().getTime();

    // Disable admin checkbox if not admin
    if (roomAdmin == false) {
        document.querySelectorAll('input[name="is-admin"]').forEach(element => {
            element.disabled = true;
        });
    };

    // Disable exclusion checkbox if not member
    if (userIsMember == false || nowInit>countDownInit) {
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
        // setTimeout('', 5000);
        location.reload();
    };

    // Set countDown
    if (document.querySelectorAll('.li-countdown').length > 0)
        setCountdown();

    // If click, set visible
    userExtracted = document.querySelector('#user-extracted');
    if (userExtracted) {
        userExtracted.onclick = function () {
            this.classList.toggle('user-extracted-not-visible');
            this.classList.toggle('user-extracted-visible');
        };
    ;}

    // Change dates
    if (roomAdmin == true) {
        // Button for display date change
        if (document.querySelector('#bnt-change-giftdate') != null) document.querySelector('#bnt-change-giftdate').onclick = function () {showDateForm('giftdate');};
        if (document.querySelector('#bnt-change-enddate') != null) document.querySelector('#bnt-change-enddate').onclick = function () {showDateForm('enddate');};
        // Dates
        if (document.querySelector('#bnt-change-giftdate') != null) document.querySelector('#bnt-change-giftdate').addEventListener("change", processInputDates);
        if (document.querySelector('#bnt-change-enddate') != null) document.querySelector('#bnt-change-enddate').addEventListener("change", processInputDates);
        
        // Button for change the date
        if (document.querySelector('#bnt-change2-giftdate') != null) document.querySelector('#bnt-change2-giftdate').onclick = function () {dateModification('giftdate');};
        if (document.querySelector('#bnt-change2-enddate') != null) document.querySelector('#bnt-change2-enddate').onclick = function () {dateModification('enddate');};
    }

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

    // Open request
    request.open('POST', url_xmasgajax_roommember_modification, false);     // the false means it's async: https://stackoverflow.com/questions/3760319/how-to-force-a-program-to-wait-until-an-http-request-is-finished-in-javascript
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrftoken)  // add csrf token for Django!
    
    // Result of request
    request.onreadystatechange = () => {
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
        if (distance < 0 && distance>-5) {
            // Reload page
            setTimeout('', 5000);
            location.reload();
        };

        }, second)
};


// Show the form for changing dates
function showDateForm (elName) {
    document.querySelectorAll('.change-'+elName).forEach(element => {
        element.classList.toggle('change-date-not-visible');
    });
};


// Input dates
function processInputDates() {
    var input = this.value;
    var dateEntered = new Date(input);
    // console.log(input); //e.g. 2015-11-13
    // console.log(dateEntered); //e.g. Fri Nov 13 2015 00:00:00 GMT+0000 (GMT Standard Time)
};



// AJAX request for changing date
function dateModification(elName) {
    // Create POST request
    var csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();

    // Open request
    request.open('POST', url_xmasgajax_date_modification, false);     // the false means it's async: https://stackoverflow.com/questions/3760319/how-to-force-a-program-to-wait-until-an-http-request-is-finished-in-javascript
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-CSRFToken", csrftoken)  // add csrf token for Django!
    
    // Result of request
    request.onreadystatechange = () => {
        // const data = JSON.parse(request.responseText);
        if (request.status == 200) 
            location.reload();
        else
            alert(request.responseText)
            // alert('Something went wrong! Try again!')
    };

    // Send
    var elDate = document.querySelector('#input-change-'+elName).value;
    var messageJson = {'roomId': room_id, 'elName': elName, 'elDate': elDate};
    request.send(JSON.stringify(messageJson));
}