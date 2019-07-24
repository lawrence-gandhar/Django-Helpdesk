var chart = c3.generate({
    bindto: '#chart',
    data: {
		x: 'x',
      	columns: line_chart_data,
    },
	axis: {
        x: {
            type: 'category',
        }
    }
});

var pie_chart = c3.generate({
	bindto: '#pie-chart',
    data: {
        columns: pie_chart_data,
        type : 'donut',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    },
});

