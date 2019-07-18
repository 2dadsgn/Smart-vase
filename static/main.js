// JavaScript Document
//slider();

function click_dx() {
	document.getElementById("chartContainer1").classList.remove("activate")
	document.getElementById("chartContainer1").classList.add("deactivate")
	document.getElementById("chartContainer2").classList.remove("deactivate")
	document.getElementById("chartContainer2").classList.add("activate")
	document.getElementById("frecciasx").classList.remove("nascosto-t")
	document.getElementById("frecciadx").classList.add("nascosto-t")
}
function click_sx() {
	document.getElementById("chartContainer2").classList.remove("activate")
	document.getElementById("chartContainer2").classList.add("deactivate")
	document.getElementById("chartContainer1").classList.remove("deactivate")
	document.getElementById("chartContainer1").classList.add("activate")
	document.getElementById("frecciasx").classList.add("nascosto-t")
	document.getElementById("frecciadx").classList.remove("nascosto-t")

}


