function loadDoc() {
  
  var date = document.getElementById("date");
  var dateparts = date.value.split("-");
  var month = dateparts[1];
  var day = dateparts[2];
  var dateobj = new Date(dateparts[0],Number(month)-1,day);
  var weekday = dateobj.getDay() !=0 ? dateobj.getDay()-1: 6;
  var hour = document.getElementById("hour").value;
  var lat = document.getElementById("lat").value;
  var lon = document.getElementById("lon").value;

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = "Number of predicted Taxi rides = " + this.responseText;
    }
  };
  
  xhttp.open("POST", "http://localhost:5000/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("month="+month+"&day="+day+"&hour="+hour+"&weekday="+weekday+"&lat="+lat+"&lon="+lon);

}