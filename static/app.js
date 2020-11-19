function updateTable() {
	url = "/api/v1/resources/pvserver/all"
	response = $.getJSON(url, function(data){
        populateTable(data);
    });
};

function populateTable(data){
    // var d = new Date();
    var r = new Array(), j = -1, counter_row = 1;
    for (key in data){
        color = (data[key]["status"] == "available") ? "green" : "red"
        console.log(color)
        r[++j] = '<tr>';
        r[++j] = `<th class="d-none d-lg-block" scope="row">${counter_row++}</th>`;
        r[++j] = `<td><code>${data[key]["name"]}</code></td>`;
        r[++j] = `<td>${data[key]["port"]}</td>`;
        // r[++j] = `<td>${d.getSeconds()}</td>`;
        r[++j] = `<td><span class="icon ${data[key]["status"]}"></span></td>`;
        r[++j] = `<td class="d-none d-lg-block" style="color: ${color}">${data[key]["status"]}</td>`;
        r[++j] = '</tr>'
    }
    $('#tableRows').html(r.join(''));
}

// Populate the table for the first time
updateTable()

// Refresh the table every 10 seconds
window.setInterval(function(){
    updateTable();
}, 10000);
