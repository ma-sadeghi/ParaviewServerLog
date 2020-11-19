$(function () {

	var tableEl = $("#test")

	url = "/api/v1/resources/pvserver/all"
	response = fetch(url);
    var data = response.json();

	console.log(data)

});

// <tr>
//   <th scope="row">{{ i+1 }}</th>
//   <td><code>pvserver{{ i+1 }}</code></td>
//   <td>{{ 11111+i }}</td>
//   <td><span class="icon {{ statuses[i] }}"></span></td>
//   <td style="color:{{ colors[i] }}">{{ statuses[i] }}</td>
// </tr>