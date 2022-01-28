let refreshButton = document.querySelector("#refreshTabelButton");
let getUsersButton = document.querySelector("#getUsersButton");
let getMeetingsButton = document.querySelector("#getAllMettingsButton");
let wrapperMeetingsTable = document.querySelector(".wrapper__meetings_table");
let actionsBar = document.querySelector(".actions_bar");


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
    

    for(let i = 0; i < resp_json.result.length; i++){
        
        let meetingBlock = document.createElement("td")
        let date = resp_json.result[i][3].split("T")
        let time_for_class = `.t${date[1].slice(0, 2)}_00`
        let topic = resp_json.result[i][2]
        meetingBlock.textContent = `${date}\n${topic}`
        
        let tableRow = document.querySelector(time_for_class)

        tableRow.appendChild(meetingBlock)
        console.log(resp_json.result[i])
    }
};

function buildTableMeetings(api_data) {
    for (let i = 0; i < api_data.lenth; i++){

        let meetingInfoElement = document.createElement("p");
        meetingInfoElement.textContent = api_data[i].join("<br>");
        tableWrapper.appendChild(meetingInfoElement)
        console.log("Building end")
    };
};

function refreshSheduledMeetings() {
    
};

async function refreshToken() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/refresh_token");
    let resp_json = await response.json();
    console.log(resp_json);
};