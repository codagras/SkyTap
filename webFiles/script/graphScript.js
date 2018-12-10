var updateInterval = 60;			//update interval in seconds
var graphUpdateInterval = 300;		//update interval in seconds
var latitude = 38.35				//latitude for sunrise/sunset calculation
var longitude = -107.38				//longitude for sunrise/sunset calculation
var chart,config;
var currentTemp;
var currentDew;
var currentGraph;

	var pad = function (x) {
		return x < 10 ? '0' + x : x;
	};

	var updateWx = function () {
		var times = SunCalc.getTimes(new Date(), latitude, longitude)
		var sunriseStr = to12hour(times.sunrise.getHours() + ':' + pad(times.sunrise.getMinutes()));
		var sunsetStr = to12hour(times.sunset.getHours() + ':' + pad(times.sunset.getMinutes()));
		
		$.ajax({
			url: 'now.json',
			cache: false,
			dataType: 'json',
			success: function (resp) {
				lastupdate = resp.now[1]
				currentTemp = resp.now[2]
				currentDew = resp.now[4]
				currentWind = resp.now[6]
				currentGust = resp.now[7]
				currentInTemp = resp.now[8]
				currentInHum = resp.now[9]
				currentRelH = resp.now[3]
				currentPressure = resp.now[11]
				todaysWindRun = resp.now[12]
				
				lastupdate = to12hour(lastupdate);
				
				$('span#lastUpdate').text(lastupdate);
				$('span#outTemp').text(currentTemp);
				$('span#outDew').text(currentDew);
				$('span#wind').text(currentWind);
				$('span#gust').text(currentGust);
				$('span#outRelH').text(currentRelH);
				$('span#pressure').text(currentPressure);
				$('span#windRun').text(todaysWindRun);
				$('span#sunriseStr').text(sunriseStr);
				$('span#sunsetStr').text(sunsetStr);
				$('span#inTemp').text(currentInTemp);
				$('span#inHum').text(currentInHum);
			}
		});
		
		$.ajax({
			url: 'records.json',
			cache: false,
			dataType: 'json',
			success: function (resp) {
				dayHighTemp = resp.records[0].toFixed(1)
				dayLowTemp = resp.records[1].toFixed(1)
				dayTempRange = (dayHighTemp - dayLowTemp).toFixed(1)
				dayHighWind = resp.records[2].toFixed()
				dayHighGust = resp.records[3].toFixed()
				dayHighPressure = resp.records[4].toFixed(1)
				dayLowPressure = resp.records[5].toFixed(1)
				monthHighTemp = resp.records[6].toFixed(1)
				monthLowTemp = resp.records[7].toFixed(1)
				monthHighRange = resp.records[8].toFixed(1)
				monthLowMax = resp.records[9].toFixed(1)
				monthHighWind = resp.records[10].toFixed()
				monthHighGust = resp.records[11].toFixed()
				monthWindrun = resp.records[12].toFixed()
				monthHighPressure = resp.records[13].toFixed(1)
				monthLowPressure = resp.records[14].toFixed(1)
				yearHighTemp = resp.records[15].toFixed(1)
				yearLowTemp = resp.records[16].toFixed(1)
				yearHighRange = resp.records[17].toFixed(1)
				yearLowMax = resp.records[18].toFixed(1)
				yearHighWind = resp.records[19].toFixed()
				yearHighGust = resp.records[20].toFixed()
				yearWindrun = resp.records[21].toFixed()
				yearHighPressure = resp.records[22].toFixed(1)
				yearLowPressure = resp.records[23].toFixed(1)
				$('span#dayHighTemp').text(dayHighTemp);
				$('span#dayLowTemp').text(dayLowTemp);
				$('span#dayHighWind').text(dayHighWind);
				$('span#dayHighGust').text(dayHighGust);
				$('span#dayHighPressure').text(dayHighPressure);
				$('span#dayLowPressure').text(dayLowPressure);
				$('span#monthHighTemp').text(monthHighTemp);
				$('span#monthLowTemp').text(monthLowTemp);
				$('span#monthHighRange').text(monthHighRange);
				$('span#monthLowMax').text(monthLowMax);
				$('span#monthHighWind').text(monthHighWind);
				$('span#monthHighGust').text(monthHighGust);
				$('span#monthWindrun').text(monthWindrun);
				$('span#monthHighPressure').text(monthHighPressure);
				$('span#monthLowPressure').text(monthLowPressure);
				$('span#yearHighTemp').text(yearHighTemp);
				$('span#yearLowTemp').text(yearLowTemp);
				$('span#yearHighRange').text(yearHighRange);
				$('span#yearLowMax').text(yearLowMax);
				$('span#yearHighWind').text(yearHighWind);
				$('span#yearHighGust').text(yearHighGust);
				$('span#yearWindrun').text(yearWindrun);
				$('span#yearHighPressure').text(yearHighPressure);
				$('span#yearLowPressure').text(yearLowPressure);
				$('span#dayTempRange').text(dayTempRange);
			}
		});
	};
	
	var to12hour = function (hour24) {
		timeArr = hour24.split(":");
		if (timeArr[0] > 12) {
			hour = String(timeArr[0] - 12);
			hour12 = hour.concat(":",timeArr[1]," PM");
		} else {
			hour = String(timeArr[0]);
			hour12 = hour.concat(":",timeArr[1]," AM");
				};
		return hour12;
	};		

	function changeGraph(graph) {
		switch (graph) {
			case 'temp':
				doTemp();
				break;
			case 'dailytemp':
				doDailyTemp();
				break;
			case 'press':
				doPress();
				break;
			case 'wind':
				 doWind();
				 break;
			case 'humidity':
				 doHum();
				 break;
			case 'dailyintemp':
				 doDailyInTemp();
				 break;
			case 'dailywindrun':
				 doDailyWindRun();
				 break;
			}
	}

	var doTemp = function () {
		currentGraph = "doTemp";
		var freezing = config.temp.units === 'C' ? 0 : 32;
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Temperature'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Temperature (°' + config.temp.units + ')'},
					opposite: false,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= freezing ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					},
					plotLines: [{
							// freezing line
							value: freezing,
							color: 'rgb(0, 0, 180)',
							width: 1,
							zIndex: 2
						}]
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: '°' + config.temp.units,
				valueDecimals: config.temp.decimals,
				xDateFormat: "%A, %b %e, %H:%M"
			},
			series: [{
					name: 'Temperature',
					zIndex: 99  
				}, {
					name: 'Dew Point',
					visible: false
				}, {
					name: 'Inside',
					visible: false
				}],
		};
		
		chart = new Highcharts.chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'tempData.json',
			cache: false,
			dataType: 'json',
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.temp);
				chart.series[1].setData(resp.dew);
				chart.series[2].setData(resp.inTemp);
			}
		});
	};

	var doPress = function() {
		currentGraph = "doPress";
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Pressure'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Pressure (' + config.press.units + ')'},
					opposite: false,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}                
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: config.press.units,
				valueDecimals: config.press.decimals,
				xDateFormat: "%A, %b %e, %H:%M"
			},
			series: [{
					name: 'Pressure'                
				}],
		};
		
		chart = new Highcharts.Chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'presData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.pres);
			}
		});
	};


	var doWind = function() {
		currentGraph = "doWind";
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Wind Speed'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Wind Speed ('+config.wind.units+')'},
					opposite: false,
					min:0,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}                
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					min:0,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: config.wind.units,
				valueDecimals: config.wind.decimals,
				xDateFormat: "%A, %b %e, %H:%M"
			},
			series: [{
					name: 'Wind Speed'
				}, {
					name: 'Wind Gust'
				}],
		};
		
		chart = new Highcharts.chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'windData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.ave_wind);
				chart.series[1].setData(resp.gust);
			}
		});
	};


	var doHum = function() {
		currentGraph = "doHum";
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Relative Humidity'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Humidity (%)'},
					opposite: false,
					min:0,
					max:100,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}                
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					min:0,
					max:100,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: '%',
				valueDecimals: config.hum.decimals,
				xDateFormat: "%A, %b %e, %H:%M"
			},
			series: [{
					name: 'Outdoor Humidity'
				}, {
					name: 'Indoor Humidity'
				}],
		};
		
		chart = new Highcharts.chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'humidityData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.relH);
				chart.series[1].setData(resp.inRelH);
			}
		});
	};

	var doDailyTemp = function () {
		currentGraph = "doDailyTemp";
		var freezing = config.temp.units === 'C' ? 0 : 32;
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Daily Outdoor Temperatures'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Daily Temperature (°' + config.temp.units + ')'},
					opposite: false,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					},
					plotLines: [{
							// freezing line
							value: freezing,
							color: 'rgb(0, 0, 180)',
							width: 1,
							zIndex: 2
						}]
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: '°' + config.temp.units,
				valueDecimals: config.temp.decimals,
				xDateFormat: "%A, %b %e"
			},
			series: [{
					name: 'Avg Temp',
					color: 'green'
				}, {
					name: 'Min Temp',
					color: 'blue'
				}, {
					name: 'Max Temp',
					color: 'red'
				}]
		};
		
		chart = new Highcharts.chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'dailyTempData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.ave);
				chart.series[1].setData(resp.min);
				chart.series[2].setData(resp.max);
			}
		});
	};
	
	var doDailyInTemp = function () {
		currentGraph = "doDailyInTemp";
		var freezing = config.temp.units === 'C' ? 0 : 32;
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Daily Indoor Temperatures'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Daily Temperature (°' + config.temp.units + ')'},
					opposite: false,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					},
					plotLines: [{
							// freezing line
							value: freezing,
							color: 'rgb(0, 0, 180)',
							width: 1,
							zIndex: 2
						}]
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: '°' + config.temp.units,
				valueDecimals: config.temp.decimals,
				xDateFormat: "%A, %b %e"
			},
			series: [{
					name: 'Avg Temp',
					color: 'green'
				}, {
					name: 'Min Temp',
					color: 'blue'
				}, {
					name: 'Max Temp',
					color: 'red'
				}]
		};
		
		chart = new Highcharts.chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'dailyInTempData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.ave);
				chart.series[1].setData(resp.min);
				chart.series[2].setData(resp.max);
			}
		});
	};
	
	var doDailyWindRun = function() {
		currentGraph = "doDailyWindRun";
		var options = {
			chart: {
				renderTo: 'chartcontainer',
				type: 'line',
				alignTicks: false
			},
			title: {text: 'Daily Windrun'},
			credits: {enabled: false},
			xAxis: {
				type: 'datetime',
				ordinal: false,
				dateTimeLabelFormats: {
					day: '%e %b',
					week: '%e %b %y',
					month: '%b %y',
					year: '%Y'
				}
			},
			yAxis: [{
					// left
					title: {text: 'Windrun (' + config.windrun.units + ')'},
					opposite: false,
					labels: {
						align: 'right',
						x: -5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}                
				}, {
					// right
					linkedTo: 0,
					gridLineWidth: 0,
					opposite: true,
					title: {text: null},
					labels: {
						align: 'left',
						x: 5,
						formatter: function () {
							return '<span style="fill: ' + (this.value <= 0 ? 'blue' : 'red') + ';">' + this.value + '</span>';
						}
					}
				}],
			legend: {enabled: true},
			plotOptions: {
				series: {
					dataGrouping:{
						enabled:false
					},
					states: {
						hover: {
							halo: {
								size: 5,
								opacity: 0.25
							}

						}
					},
					cursor: 'pointer',
					marker: {
						enabled: false,
						states: {
							hover: {
								enabled: true,
								radius: 0.1
							}
						}
					}
				},
				line: {lineWidth: 2}
			},
			tooltip: {
				shared: true,
				crosshairs: true,
				valueSuffix: config.windrun.units,
				valueDecimals: config.windrun.decimals,
				xDateFormat: "%A, %b %e, %H:%M"
			},
			series: [{
					name: 'Windrun'                
				}],
		};
		
		chart = new Highcharts.Chart(options);
		chart.showLoading();
		
		$.ajax({
			url: 'dailyWindRunData.json',
			dataType: 'json',
			cache: false,
			success: function (resp) {
				chart.hideLoading();
				chart.series[0].setData(resp.windRun);
			}
		});
	};
	
$(document).ready(function () { 

	$.ajax({url: "graphconfig.json", dataType:"json", success: function (result) {
			config=result;
				updateWx();
				doTemp();
	
	}});
	
	var ticktock = function () {
        var d = new Date();
		
		$('span#time').text(d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }));
		$('span#date').text(d.toDateString());

    };
	
	var updateGraph = function () {
		window[currentGraph]();
	};
	
	// do Ajax update
	updateWx();
	
	// start the timer for the display and graph updates
	setInterval(updateWx, updateInterval * 1000);
	setInterval(updateGraph, graphUpdateInterval * 1000);

    ticktock();

    // Calling ticktock() every 10 seconds
    setInterval(ticktock, 10000);
});
