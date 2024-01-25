<?php
	require_once('color_hash.php');

	$db = new SQLite3('data.sqlite', SQLITE3_OPEN_READONLY);

	function print_post_head($p){
		$c = ids2color($p['capcode']);
		?>
			<div class="post_head">
				<span class='subject'><?=$p['subject']?></span>
				<span class='name'><?=$p['name']?></span>
				<a class='post_no'>No. <?=$p['id']?></a>
				<span class='poster_id' style="background: <?=$c[0]?>; color: <?=$c[1]?>">ID <?=strtoupper($p['capcode'])?></span>
				<span class='date'><?=$p['time']?></span>
			</div>
		<?php
	}

	function print_file($f){
		$mt = mime_content_type($f['path']);
		?>
			<div class='file'>
				<div><?=$f['name']?></div>
		<?php
			if(strpos($mt, 'image/') === 0):
		?>
				<img src='<?=$f['path']?>'></img>
		<?php
			elseif(strpos($mt, 'video/') === 0):
		?>
				<video src='<?=$f['path']?>'></video>
		<?php
			endif;
		?>
			</div>
		<?php
	}

	function print_files($no, $board){
		global $db;
		$query = 'SELECT * FROM files WHERE post = ' . $no . ' AND board = \'' . $board . '\' ORDER BY id;';
		$files = $db->query($query);
		if($files){
			while($f = $files->fetchArray()){
				print_file($f);
			}
		}
	}

	function validate_board_name($s){
		global $db;
		$result = $db->query('SELECT name FROM boards;');
		$boards = array();
		while($row = $result->fetchArray()){
			array_push($boards, $row['name']);
		}

		return in_array('/'.$s.'/', $boards);
	}
?>
