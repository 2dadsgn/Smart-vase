// JavaScript Document
//slider();

function click_dx() {
	document.getElementById("chartContainer1").classList.remove("activate")
	document.getElementById("chartContainer1").classList.add("deactivate")
	document.getElementById("chartContainer2").classList.remove("deactivate")
	document.getElementById("chartContainer2").classList.add("activate")
}
function click_sx() {
	document.getElementById("chartContainer2").classList.remove("activate")
	document.getElementById("chartContainer2").classList.add("deactivate")
	document.getElementById("chartContainer1").classList.remove("deactivate")
	document.getElementById("chartContainer1").classList.add("activate")

}



function slider(){
	setInterval("bkgrnd_1()",55000);
	setInterval("bkgrnd_2()",125000);
	setInterval("bkgrnd_3()",175000);
	setInterval("bkgrnd_4()",230000);
	
}

function bkgrnd_1(){
	var	main=document.getElementById("container");
	main.style.backgroundImage="url('bkg(1).jpg')";
}
function bkgrnd_2(){
	var	main=document.getElementById("container");
	main.style.backgroundImage="url('bkg (2).jpg')";
}
function bkgrnd_3(){
	var	main=document.getElementById("container");
	main.style.backgroundImage="url('bkg (3).jpg')";
}
function bkgrnd_4(){
	var	main=document.getElementById("container");
	main.style.backgroundImage="url('bkg (4).jpg')";
}

