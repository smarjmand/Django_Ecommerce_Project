// var messageTimer = document.getElementById("message-timer");
// setTimeout(function () {
//     messageTimer.style.display = "none";
// }, 3000)

document.addEventListener('DOMContentLoaded', function () {
    var messageTimer = document.getElementById("message-timer");
    if (messageTimer) {
        setTimeout(function () {
            messageTimer.style.display = "none";
        }, 4000);
    } else {
        console.log('No message to display.');
    }
});