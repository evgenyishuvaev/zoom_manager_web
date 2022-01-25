let refreshButton = document.querySelector("#refreshTabelButton");
let getUsersButton = document.querySelector("#getUsersButton");
let getMeetingsButton = document.querySelector("#getAllMettingsButton");

refreshButton.addEventListener("click", refreshToken, false);
getUsersButton.addEventListener("click", getZoomUsers, false);
getMeetingsButton.addEventListener("click", getAllMeetings, false);

// document.querySelector(".wrapper__meetings_table").innerHTML = `<table class="meetings_table"></table>`

async function getZoomUsers() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/users");
    let resp_json = await response.json();
    console.log(resp_json);
};


async function getAllMeetings() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/all_meetings");
    let resp_json = await response.json();
    console.log(resp_json);
};

function buildTableMeetings(api_data) {

};

function refreshSheduledMeetings() {
    
};

async function refreshToken() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/refresh_token");
    let resp_json = await response.json();
    console.log(resp_json);
};