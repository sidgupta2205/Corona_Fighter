
<html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="../css/style.css">
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
      </div>
  <br>
  <br>
    </body>
  </html>
  
    

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
  
  
  