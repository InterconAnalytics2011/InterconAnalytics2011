jQuery(document).ready(function() {
    jQuery.ajax({
        url: '/data/last-year-visits',
        success: function(data){
            jQuery('#last-year-visits').removeClass('slot');
            jQuery('#last-year-visits').html(data + 'Mi');
            
            var lyv = data;   
            
            jQuery.ajax({
                url: '/data/current-year-visits',
                context:{lyv: lyv},
                success: function(data){
                    jQuery('#current-year-visits').removeClass('slot');
                    jQuery('#current-year-visits').html(data + 'Mi');
                    
                    var percent = (parseFloat(data) * 100) / parseFloat(this.lyv);
                    
                    if(percent < 100) {
                        jQuery('#percent-current-year-vists').addClass('down');
                    } else {
                        jQuery('#percent-current-year-vists').addClass('up');
                    }
                    
                    jQuery('#percent-current-year-vists').removeClass('slot');
                    jQuery('#percent-current-year-vists').html( percent.toFixed(0) + '%');
                    
                }
            });
        }
    });
});

function ShortNumFormater(){
	return true;
}
ShortNumFormater.prototype.format = function(data,col){
	for (var i=0; i < data.getNumberOfRows(); i++){
		try{
			if(parseInt(data.getValue(i,col),10) >= 1000000){
				data.setFormattedValue(i, col, parseInt(data.getValue(i,col),10)/(1000*1000) + ' Mi');
				data.setValue(i, col, parseInt(data.getValue(i,col),10)/(1000*1000));
			}else if(parseInt(data.getValue(i,col),10) >= 1000){
				data.setFormattedValue(i, col, parseInt(data.getValue(i,col),10)/(1000) + ' K');
				data.setValue(i, col, parseInt(data.getValue(i,col),10)/(1000));
			}
		}catch(e){}
	} 
}

function draw_s1(){
	this.get_data();
}

function get_data_s1() {
	var i = null;

	clearInterval(this.timer_reload);
	this.timer_reload = setInterval(this.draw, 1000 * this.refreshInterval);

	// Query data source
	for (i in this.charts){
		i = this.charts[i];
		try{
			i.query.send(i.handler);
		}catch(e){}
	}
}

// Chart 1: Last month New / Returning
function handle_s1_c1(response) {
	var c = dash.s1.charts[0];
	if (response.isError()) {
		if(console && console.log){
			console.log('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		}
		if(response.getReasons() && response.getReasons()[0] === 'internal_error'){
			c.query.send(arguments.callee);
		}
		return;
	}
	//Store data
	c.data = response.getDataTable();

	//Draw charts if visible
	if(dash.current_slide === 1){
		c.draw();
	}
	jQuery('#' + dash.s1.el).bind('show_slide', c.draw);
}
function draw_s1_c1(){
	var c = dash.s1.charts[0];
	var options = {
        is3D: true,
        legend: 'bottom',
        backgroundColor: 'none',
        title: 'Mês anterior'
	};

	jQuery('#'+c.el).html('');
    
	c.chart = new google.visualization.PieChart(jQuery('#' + c.el).get(0));

	try{
		c.chart.draw(c.data, options);
        jQuery('#' + c.el).removeClass('slot');
	}catch(e){
		//No data yet. It will be called once the data is ready
	}
}


// Chart 2: Current month New / Returning
function handle_s1_c2(response) {
	var c = dash.s1.charts[1];
	if (response.isError()) {
		if(console && console.log){
			console.log('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		}
		if(response.getReasons() && response.getReasons()[0] === 'internal_error'){
			c.query.send(arguments.callee);
		}
		return;
	}
	//Store data
	c.data = response.getDataTable();

	//Draw charts if visible
	if(dash.current_slide === 1){
		c.draw();
	}
	jQuery('#' + dash.s1.el).bind('show_slide', c.draw);
}
function draw_s1_c2(){
	var c = dash.s1.charts[1];
	var options = {
        is3D: true,
        legend: 'bottom',
        backgroundColor: 'none',
        title: 'Mês atual'
	};

	jQuery('#'+c.el).html('');
    
	c.chart = new google.visualization.PieChart(jQuery('#' + c.el).get(0));

	try{
		c.chart.draw(c.data, options);
        jQuery('#' + c.el).removeClass('slot');
	}catch(e){
		//No data yet. It will be called once the data is ready
	}
}


// Chart 3: Visits
function handle_s1_c3(response) {
	var c = dash.s1.charts[2];
	if (response.isError()) {
		if(console && console.log){
			console.log('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		}
		if(response.getReasons() && response.getReasons()[0] === 'internal_error'){
			c.query.send(arguments.callee);
		}
		return;
	}
	//Store data
	c.data = response.getDataTable();

	//Draw charts if visible
	if(dash.current_slide === 1){
		c.draw();
	}
	jQuery('#' + dash.s1.el).bind('show_slide', c.draw);
}
function draw_s1_c3(){
	var c = dash.s1.charts[2];
	var options = {
        backgroundColor: 'none',
		legend: 'bottom',
		seriesType: 'bars',
		series: {1: {type: 'line'}},
        hAxis: {textStyle: {fontSize: '10'}}
	};

	jQuery('#' + c.el).html('');
    
	c.chart = new google.visualization.ComboChart(jQuery('#' + c.el).get(0));

	try{
		c.chart.draw(c.data, options);
        jQuery('#' + c.el).removeClass('slot');
	}catch(e){
		//No data yet. It will be called once the data is ready
	}
}

//format thousands
function splitThousand(val, axis)
{
	val += '';
	x = val.split('.');
	x1 = x[0];
	x2 = x.length > 1 ? '.' + x[1] : '';
	var rgx = /(\d+)(\d{3})/;
	while (rgx.test(x1)) {
		x1 = x1.replace(rgx, '$1' + '.' + '$2');
	}
	return x1 + x2;
}

// add a percent symbol to axis
function percent(val, axis) {
	return val.toFixed(axis.tickDecimals) + " %";
}

// Slide namespace
var dash = dash || {};
dash.s1 = {
	timer_reload:null,
	el: 'slide-1',
	refreshInterval: 60*60*8, //8 hours
	charts: [
		{
			el: 'last-month-visitors', // element matching to elemnt id
			handler: handle_s1_c1, // reference to handler function
			draw: draw_s1_c1,
			chart: null, // reference to chart object
			data: null, // data response object
			query: new google.visualization.Query('/data/last-month-new-returning')
		},{
			el: 'current-month-visitors', // element matching to element id
			handler: handle_s1_c2, // reference to handler function
			draw: draw_s1_c2,
			chart: null, // reference to chart object
			data: null, // data response object
			query: new google.visualization.Query('/data/current-month-new-returning')
		},{
			el: 'month-visits', // element matching to element id
			handler: handle_s1_c3, // reference to handler function
			draw: draw_s1_c3,
			chart: null, // reference to chart object
			data: null, // data response object
			query: new google.visualization.Query('/data/visits')
		}
	],
	get_data: get_data_s1, // draw/updates graphs
	draw: draw_s1 // supposed to be called once
};

// vim: encoding=utf8