var loadFile = function(event) {
    document.getElementById('submit').disabled = false;
    document.getElementById('submit').style.backgroundColor='#ff0000';
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
};