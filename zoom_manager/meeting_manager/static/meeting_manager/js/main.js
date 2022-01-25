let refreshButton = document.querySelector("#refreshTabelButton")
refreshButton.addEventListener("click", refreshToken, false)

// document.querySelector(".wrapper__meetings_table").innerHTML = `<table class="meetings_table"></table>`

function getDataMeetings() {
    
}

function buildTableMeetings(api_data) {

}

function refreshSheduledMeetings() {
    
}

function refreshToken() {
    let promise = fetch("http://127.0.0.1:8000/meeting_manager/api/refresh_token")
    alert(promise.JSON)
}