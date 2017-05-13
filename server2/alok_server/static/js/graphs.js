function delay(ms) {
   ms += new Date().getTime();
   while (new Date() < ms){}
}

function getScreePlot() {
	delay(500);
	d3.select("#chart").selectAll("img").remove();
	d3.select("#chart").append("img").attr("src", "/static/images/ScreePlot.png").attr("width", "1000").attr("height", "500");
}


function getPCALoadings() {
	delay(500);
	d3.select("#chart").selectAll("img").remove();
	sel = document.getElementById('myselect');
	if(sel.options[sel.selectedIndex].value == "random")
		d3.select("#chart").append("img").attr("src", "/static/images/PCA_Loading_Random.png").attr("width", "1000").attr("height", "500");
	else
		d3.select("#chart").append("img").attr("src", "/static/images/PCA_Loading_Stratified.png").attr("width", "1000").attr("height", "500");
}

function getPCA() {
	delay(800);
	setTimeout(d3.select("#chart").selectAll("img").remove(), 5000);
	sel = document.getElementById('myselect');
	if(sel.options[sel.selectedIndex].value == "random")
		d3.select("#chart").append("img").attr("src", "/static/images/ScatterPlot_Random.png").attr("width", "1000").attr("height", "500");
	else
		d3.select("#chart").append("img").attr("src", "/static/images/ScatterPlot_Stratified.png").attr("width", "1000").attr("height", "500");
}

function getMDS_Euclidean() {
	delay(1500);
	d3.select("#chart").selectAll("img").remove();
	if(sel.options[sel.selectedIndex].value == "random")
		d3.select("#chart").append("img").attr("src", "/static/images/MDS_Random_Euclidean.png").attr("width", "1000").attr("height", "500");
	else
		d3.select("#chart").append("img").attr("src", "/static/images/MDS_Stratified_Euclidean.png").attr("width", "1000").attr("height", "500");
}

function getMDS_Correlation() {
	delay(1500);
	d3.select("#chart").selectAll("img").remove();
	if(sel.options[sel.selectedIndex].value == "random")
		d3.select("#chart").append("img").attr("src", "/static/images/MDS_Random_Correlation.png").attr("width", "1000").attr("height", "500");
	else
		d3.select("#chart").append("img").attr("src", "/static/images/MDS_Stratified_Correlation.png").attr("width", "1000").attr("height", "500");
}

function getScatterPlotMatrix() {
	delay(1000);
	d3.select("#chart").selectAll("img").remove();
	if(sel.options[sel.selectedIndex].value == "random")
		d3.select("#chart").append("img").attr("src", "/static/images/ScatterPlotMatrix-Random.png").attr("width", "1000").attr("height", "500");
	else
		d3.select("#chart").append("img").attr("src", "/static/images/ScatterPlotMatrix-Stratified.png").attr("width", "1000").attr("height", "500");
}

