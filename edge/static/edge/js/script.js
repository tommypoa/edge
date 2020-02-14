// Set-up

var canvas = document.getElementById("im1");
var ctx = canvas.getContext("2d");
ctx.fillStyle = "#FF0000";

var canvas2 = document.getElementById("im2");
var ctx2 = canvas2.getContext("2d");
ctx2.fillStyle = "#00FF00";

var curX, curY;
var curX2, curY2;

var canvas_data = { "coordinates": []};

// var width = canvas.width, height = canvas.height;
// var fill_value = true, stroke_value = false;
// ctx.lineWidth = 2;

// Tuning parameters

var tuningX = -6
var tuningY = -4

// Helper Functions

function onload1() {
    var background = new Image();
    background.src = document.currentScript.getAttribute("img");
    background.onload = () => {
    ctx.drawImage(background, 0, 0, 512, 512);   
    }
}
function onload2() {
    var background = new Image();
    background.src = document.currentScript.getAttribute("img2");
    background.onload = () => {
    ctx2.drawImage(background, 0, 0, 512, 512);   
    }
}

function listen() {
    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft + tuningX;
        curY = e.clientY - canvas.offsetTop + tuningY;
        hold = true;
        ctx.fillRect(curX,curY,3,3);
    }

    canvas2.onmousedown = function (e){
        curX2 = e.clientX - canvas2.offsetLeft + tuningX;
        curY2 = e.clientY - canvas2.offsetTop + tuningY;
        hold = true;
        ctx2.fillRect(curX2,curY2,3,3);
    }
}

// Main execution
onload1();
onload2();
listen();