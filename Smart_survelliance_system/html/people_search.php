
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="../css/style.css">

<style>
#fade {
    display: none;
    position:absolute;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 100%;
    background-color: #ababab;
    z-index: 1001;
    -moz-opacity: 0.8;
    opacity: .70;
    filter: alpha(opacity=80);
}

#modal {
    display: none;
    
}
</style>
</head>
<body>
<div class="navbar">
  <a href="Live_page.html">LIVE VIEW</a>
  <a href="crowd_alert.html">CROWD ALERT</a>
  <a href="people_search.php">PEOPLE SEARCH</a>
  <div class="dropdown">
    <button class="dropbtn">QURANTINE PERSON TRACK 
      <i class="fa fa-caret-down"></i>
    </button>
    <div class="dropdown-content">
      <a href="Add_person_track.php">ADD PERSON TO TRACK</a>
      <a href="Real_time_alert.html">REAL TIME ALERT</a>
    </div>
  </div> 
</div>
<br>
<br>
<div>
  <form action="/Corona_Fighter/html/people_search.php" method="post" enctype="multipart/form-data">
    Select image to upload:
    <input type="file" name="fileToUpload" id="fileToUpload">
    <input type="submit" value="Upload Image" name="submit">
  </form>  
  Name:<input type="input" id="name">
  <button  onclick="httpGetAsync()">SEARCH NOW</button>
</div>
<br>
<br>
<div id="Images">
</div>
<div id="fade"></div>
<div id="modal">
<h5>Please wait while the search is loading</h5>
<img id="loader" src="Loading_icon.gif" />
</div>
</body>
</html>


<script>
function myFunction(arr) {
    var out = "";
    var i;
    var val;
    path = "../micro_server/"
        //alert(arr.length);
    for(var key in arr) {
    currfile = arr[key].split("/")
		filenam = currfile[currfile.length-1]
		filenam = filenam.split("_")
		camname = filenam[0]
        var add = arr[key].split("_")
        out += '<img src="'+ path+ arr[key] + '" height="300" width="400"/><h3>Last Seen at '+camname+' Location</h3>';
    }
    document.getElementById("Images").innerHTML = out;
}

function openModal() {
        document.getElementById('modal').style.display = 'block';
        document.getElementById('fade').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('fade').style.display = 'none';
}


    function httpGetAsync()
    {
        openModal()
        var name = document.getElementById("name").value
        var theUrl = 'http://localhost:5081/?cmd=people_search&name='+name
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            {
                closeModal()
                var myArr = JSON.parse(xmlHttp.responseText)
                myFunction(myArr)
                
            }
        }
        xmlHttp.open("GET", theUrl, true); // true for asynchronous 
        xmlHttp.send();

    }
     
</script>

<?php
if(!empty($_FILES['fileToUpload']))
{
$target_dir = "uploads/";
$target_file = $target_dir.basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// Check if file already exists
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
  echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    $zip = new ZipArchive;
    $res = $zip->open($target_file);
if ($res === TRUE) {
  $zip->extractTo('../FaceRecog/dataset/');
  $zip->close();
  echo 'woot!';
} else {
  echo 'doh!';
}
  } else {
    echo "Sorry, there was an error uploading your file.";
  }
}
}
?>


