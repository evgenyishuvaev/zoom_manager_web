// let refreshButton = document.querySelector("#refreshTabelButton");
let getUsersButton = document.querySelector("#getUsersButton");
let getMeetingsButton = document.querySelector("#getAllMettingsButton");

let formCancelButton = document.getElementById('meeting_cancel_creation')
let formOverlay = document.querySelector(".overlay")
let csrfTokenInput = document.getElementById("csrftoken")
let accountInput = document.getElementById('meeting_host_id')
let whenDateInput = document.getElementById('meeting_date')
let whenTimeInput = document.getElementById('meeting_time')    

let wrapperMeetingsTable = document.querySelector(".wrapper__meetings_table");
let actionsBar = document.querySelector(".actions_bar");
let columnName = document.querySelector(".column_name")

let timeRowClass = [
    ".t08", ".t09", ".t10", ".t11", ".t12", ".t13",
    ".t14", ".t15", ".t16", ".t17", ".t18", ".t19", ".t20"
]


// refreshButton.addEventListener("click", refreshButton, false);
document.addEventListener("DOMContentLoaded", buildTable, false);
getMeetingsButton.addEventListener("click", getAllMeetings, false);
getUsersButton.addEventListener("click", getUsersFromZoom, false)
formCancelButton.addEventListener("click", hideCreatingForm, false)

async function getUsersFromZoom() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/v1/users_zoom")
    let resp_json = await response.json()
    console.log(resp_json)
}

async function hideCreatingForm() {
    formOverlay.classList.remove("overlayShow")
}

async function buildTable() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/v1/users");
    let resp_json = await response.json();
    console.log(resp_json);

    for (host_id in resp_json){

        if (document.getElementById(`user:${host_id}`) == null){

            console.log("Я в условии")
            let thName = document.createElement("th")
            thName.textContent = `${resp_json[host_id]}`
            thName.id = `user:${host_id}`

            columnName.appendChild(thName)

            console.log("Я перехожу к второму циклу")
            for(let i = 0; i < timeRowClass.length; i++){
                let timeRow = document.querySelector(`${timeRowClass[i]}`)
                let host_idCell = document.createElement("td")
                let host_idButton = document.createElement("button")
                host_idButton.id = `btn:${host_id}${timeRowClass[i]}`
                host_idButton.classList.add('create_btn') 
               
                host_idButton.textContent = "+"               
                host_idButton.addEventListener('click', createMeeting, false)

                host_idCell.id = `cell:${host_id}${timeRowClass[i]}`
                timeRow.appendChild(host_idCell)
                
                host_idCell.appendChild(host_idButton)
            }
        }
    }

    getAllMeetings()
}


async function getAllMeetings() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/v1/all_meetings");
    let resp_json = await response.json();
    console.log(resp_json)
    
    if (resp_json.result == "Check your refresh_token for OAuth 2.0"){
        alert(resp_json.result)
        return
    }

    for(let i = 0; i < resp_json.result.length; i++){

        let host_id = resp_json.result[i][1]
        let date = new Date(resp_json.result[i][3])
        let time_for_class = `.t${date.getHours()}`
        let topic = resp_json.result[i][2]
        console.log(topic, host_id, date, time_for_class)

        let nowData = new Date()
        let meetingData = new Date(resp_json.result[i][3])
        
        // Сверяем дату с сегодняшней
        if (nowData.getDate() !== meetingData.getDate()){
            console.log("Пропускаем")
            continue
        }

        
        let tableCell = document.getElementById(`cell:${host_id}${time_for_class}`)
        tableCell.textContent = `${topic}`

        console.log(resp_json.result[i])
    }
};


async function createMeeting (event){
    let host_id = event.currentTarget.id.split(":")[1].slice(0,-4)
    let time = event.currentTarget.id.split(":")[1].slice(-2)
    let emailZoomUser = document.getElementById(`user:${host_id}`).textContent
    let csrf = document.cookie.split("=")[1]

    let nowDate = new Date()

    let todayDay = nowDate.getDate()
    let todayMonth = nowDate.getMonth() + 1
    let todayFullYear = nowDate.getFullYear()

    if(todayDay.toString().length == 1){
        todayDay = `0${todayDay}`
    }
    if(todayMonth.toString().length == 1){
        todayMonth = `0${todayMonth}`
    }

    formOverlay.classList.add("overlayShow")

    csrfTokenInput.setAttribute("value", csrf)
    accountInput.setAttribute("value", emailZoomUser)
    whenDateInput.setAttribute("value", `${todayFullYear}-${todayMonth}-${todayDay}`)
    whenTimeInput.setAttribute("value", `${time}:00:00`)

    console.log(host_id, time, emailZoomUser, csrf, `${todayFullYear}-${todayMonth}-${todayDay}`)
}


// async function refreshToken() {
//     let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/v1/refresh_token");
//     let resp_json = await response.json();
//     console.log(resp_json);
// };

