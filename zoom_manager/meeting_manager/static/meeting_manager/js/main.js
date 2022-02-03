// let refreshButton = document.querySelector("#refreshTabelButton");
let getUsersButton = document.querySelector("#getUsersButton");
let getMeetingsButton = document.querySelector("#getAllMettingsButton");

let wrapperMeetingsTable = document.querySelector(".wrapper__meetings_table");
let actionsBar = document.querySelector(".actions_bar");
let columnName = document.querySelector(".column_name")

let timeRowClass = [
    ".t08", ".t09", ".t10", ".t11", ".t12", ".t13",
    ".t14", ".t15", ".t16", ".t17", ".t18", ".t19", ".t20"
]


// refreshButton.addEventListener("click", refreshButton, false);
document.addEventListener("DOMContentLoaded", addZoomUsersToTable, false);
getMeetingsButton.addEventListener("click", getAllMeetings, false);
getUsersButton.addEventListener("click", getUsersFromZoom, false)


async function getUsersFromZoom() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/users_zoom")
    let resp_json = await response.json()
    console.log(resp_json)
}


async function addZoomUsersToTable() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/users");
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
                host_idButton.textContent = "Запланировать конференцию"               
                host_idButton.addEventListener('click', createMeeting, false)

                host_idCell.id = `cell:${host_id}${timeRowClass[i]}`
                timeRow.appendChild(host_idCell)
                
                host_idCell.appendChild(host_idButton)
            }
        }
    }
}


async function getAllMeetings() {
    let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/all_meetings");
    let resp_json = await response.json();
    console.log(resp_json)
    

    for(let i = 0; i < resp_json.result.length; i++){

        let host_id = resp_json.result[i][1]
        let date = new Date(resp_json.result[i][3])
        let time_for_class = `.t${date.getHours()}`
        let topic = resp_json.result[i][2]
        console.log("Я в первом цикле")
        console.log(i)

        let nowData = new Date()
        let meetingData = new Date(resp_json.result[i][3])
        
        // Сверяем дату с сегодняшней
        if (nowData.getDate() !== meetingData.getDate()){
            console.log("Пропускаем")
            continue
        }

        
        let tableCell = document.getElementById(`cell:${host_id}${time_for_class}`)
        tableCell.textContent = `${date}<br>${topic}`

        console.log(resp_json.result[i])
    }
};


async function createMeeting (event){
    let host_id = event.currentTarget.id.split(":")[1].slice(0,-4)
    let time = event.currentTarget.id.split(":")[1].slice(-4)
    console.log(host_id, time)
}


// async function refreshToken() {
//     let response = await fetch("http://127.0.0.1:8000/meeting_manager/api/refresh_token");
//     let resp_json = await response.json();
//     console.log(resp_json);
// };