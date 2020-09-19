<?php
	$servername='localhost';
	$username='id14775725_tech';
	$password='@Nkit16181618';
	$dbname = "id14775725_warrior";
	$link=mysqli_connect($servername,$username,$password,"$dbname");
	  if(!$link){
		  die('Could not linkect MySql Server:' .mysql_error());
		}
?>