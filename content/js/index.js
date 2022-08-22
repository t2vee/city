function on() {
    document.getElementById("overlay").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
}

function frgtpwdovrly() {
    document.getElementById("forgetpasswordoverlay").style.display = "block";
    document.getElementById("container").style.display = "none";
}

function frgtpwdovrlyclose() {
    document.getElementById("forgetpasswordoverlay").style.display = "none";
    document.getElementById("container").style.display = "block";
}

function copyToClipboard(elementId) {
    var aux = document.createElement("input");
    aux.setAttribute("value", document.getElementById(elementId).innerHTML);
    document.body.appendChild(aux);
    aux.select();
    document.execCommand("copy");
    document.body.removeChild(aux);
}