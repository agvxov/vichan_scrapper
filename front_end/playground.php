<?php
	require_once('global.php');
	require_once('config.php');
	$query = 'SELECT COUNT(*) count FROM posts 
				WHERE 
					board = \'/' . $_GET['board'] . '/\' 
						AND 
					thread is NULL; create table fuck_you (i int);';
	echo $query . '</br>';
	echo $db->querySingle($query) . '</br>';
?>
