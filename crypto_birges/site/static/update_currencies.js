var websocket = new WebSocket("ws://localhost:2010/");

websocket.onmessage = ({data}) => {
    parseValue(data);
};

websocket.onclose = (event) => {
    alert("Данные не обновляются");
};


websocket.onerror = (error) => {
    console.error(`Произошла ошибка ${error}`);
};


function createPair(msg) {
    let table = document.getElementById("currencies");
    let row = document.createElement("tr");
    table.appendChild(row);
};

function parseValue(msg) {
    let incomingMessage = JSON.parse(msg);
    try { 
        let allCurrencyPairs = document.querySelectorAll(`b.${incomingMessage.subject}`);
        for (let pair of allCurrencyPairs) {
            pair.innerText = incomingMessage['data']['price'];
            let parent = pair.parentNode.parentNode;
            let children = [...parent.children];
            let children_copy = children.slice(0,3);
            let values = [];
            children_copy.forEach((element) => {
                let cellNum = parseFloat(element.innerText.split(":")[1].trim());
                if (!isNaN(cellNum)) {
                    values.push(cellNum);
                };
            });
            if (values.length === 3) {
                children[3].innerText = `Total ${(values[1] / (values[0] * values[2])).toFixed(12)} USDT`;
            };
        };
    } catch (DOMException) {
        console.log(`Новая валюта ${incomingMessage.subject}`)
    }
    
};












