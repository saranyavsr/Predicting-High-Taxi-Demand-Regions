
function loadDoc() {
  var date = document.getElementById("date");
  var dateparts = date.value.split("-");
  var month = dateparts[1];
  var day = dateparts[2];
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "localhost:5000", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("month="+month+"&day"+day+"&hour=1&weekday=2&lat=1&lon=2");
}