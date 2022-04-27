/*Slides*/

const slides = ['slide0', 'slide1', 'slide2'];

function showSlide(slideName){
    slides.forEach(function (value){
        if(value == slideName){
            document.getElementById(value).style.display = "block";
        }else{
            document.getElementById(value).style.display = "none";
        }
    })
}

window.onload = function (){
    showSlide('slide0')
}

function ticketSearch(){
    console.log(document.getElementById('barcode').value)
}
