document.onload = function() {
   fetch('/status')
  .then(response => response.json())
  .then(data => console.log(data));
}

document.getElementById('start').onclick = function() {
   var speed_val = document.getElementById('speed').value
   var duration_val = document.getElementById('duration').value
   console.log(speed_val, duration_val)

   fetch('/start'+'?speed='+speed_val+'&duration='+duration_val)
  .then(response => response.json())
  .then(data => console.log(data));
}

document.getElementById('stop').onclick = function() {
   fetch('/stop')
  .then(response => response.json())
  .then(data => console.log(data));
}

document.getElementById('force').onclick = function() {
   fetch('/force')
  .then(response => response.json())
  .then(data => console.log(data));
}

function speed(val) {
    console.log(val)
    document.getElementById("speed-value").innerHTML = val
}

function duration(val) {
    console.log(val)
    document.getElementById("duration-value").innerHTML = val + " minutter"
}