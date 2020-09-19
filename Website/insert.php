<?php
session_start();

include_once 'connection.php';
if(isset($_POST['submit']))
{    
     $name = $_POST['name'];
     $gender = $_POST['gender'];
     $age = $_POST['age'];
     $mdate = $_POST['mdate'];
     $location = $_POST['location'];
     $more = $_POST['more'];
     $phone = $_POST['phone'];
     $email = $_POST['email'];

    $sql = "INSERT INTO registration (name,gender,age,mdate,location,more,phone,email)
     VALUES ('$name','$gender','$age','$mdate','$location','$more','$phone','$email')";

     if (mysqli_query($link, $sql)) {
         header("Location: insertafter.php");
     } else {
        echo "Error: " . $sql . ":-" . mysqli_error($link);
     }
     mysqli_close($link);
}
?>