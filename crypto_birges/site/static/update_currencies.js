var websocket = new WebSocket("ws://localhost:2010");

websocket.onopen = () => {
    console.log("WebSocket is open!");
};

websocket.onclose = (event) => {
    alert("Данные не обновляются");
};


websocket.onerror = (error) => {
    console.error(`Произошла ошибка ${error}`);
};


/* function createPair(msg) {
    let table = document.getElementById("currencies");
    let row = document.createElement("tr");
    table.appendChild(row);
};*/

function parseValue(msg) {
    let incomingMessage = JSON.parse(msg.data);
    let allCurrencyPairs = document.querySelectorAll(`b.${incomingMessage['pair']}`);
    for (pair of allCurrencyPairs) {
        pair.innerText = incomingMessage['price'];
    };
};


function calculateSpread() {
    // let parrentNode = document.parentNode;
    let tds = this.parentNode().children;
    let flag;
    let values = [];
    console.log(9999);
    for (let i = 0; i <= 2; i++) {
        // проверка на наличие цены
        flag = tds[i].split(":")[1].trim() === '' ? true : false;
        if (flag) {
            
            return '';
        }
       else {
            values.push(parseInt(tds[i].split(":")[1].trim().toNum));
        }
    };
    // формула для расчёта спреда
    let total = values[1] / (values[0] * values[2]);
    tds[3].innerText = total.toFixed(2) + " USDT";
};

websocket.onmessage = (event) => {
    // parseValue(event.data);
    console.log(event.data)
};