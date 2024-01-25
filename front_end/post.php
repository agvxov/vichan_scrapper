<!DOCTYPE html>
	<html>
		<?php
			require_once('global.php');

			# Query validation
			if(validate_board_name($_GET['board'])){
				$board = '/'.$_GET['board'].'/';
			}else{
				header('Location: /404.php');
				die();
			}
		?>
		<head>
			<title>Examplechan - Archive /<?=$board?>/<?=$_GET['post']?></title>
			<link rel="stylesheet" href="global.css">
			<meta charset="utf-8">
			<script type="text/javascript" src="js/jquery.min.js"></script>
			<script type="text/javascript" src="js/show-op.js"></script>
			<style>
				#body_main {
					margin-bottom: 200px;
				}
				.post img {
					width: 100%;
				}
			</style>
		</head>
		<body>
			<div id=body_main>
				<div id=index_header>
					<p>Examplechan Archive - /<?=$board?>/</p>
					<p>Thread No. <?=$_GET['post']?><p>
					<a href="/">
						<img id=plant src="media/plant.png" alt="fc_logo"></img>
					</a>
				</div>
				<hr>
				<hr>
				<!-- ###### -->
				<div class="op post">
					<?php
						$query = 'SELECT * FROM posts WHERE id = ' . $_GET['post'] . ' AND board = \'' . $board . '\';';
						$thread = $db->query($query)->fetchArray();
					?>
					<div class='files'>
						<?=print_files($thread['id'], $thread['board'])?>
					</div>
					<?=print_post_head($thread)?>
					<div class='post_body'>
						<?=$thread['body']?>
					</div>
				</div>
				<!-- ###### -->
				<?php
					$posts = $db->query('SELECT * FROM posts WHERE thread = ' . $thread['id'] . ' AND board = \'' . $board  . '\';');
					while($p = $posts->fetchArray()):
				?>
				<hr>
					<div class="reply post">
						<?=print_post_head($p)?>
						<div class='files'>
							<?=print_files($p['id'], $p['board'])?>
						</div>
						<div class='post_body'>
							<?=$p['body']?>
						</div>
					</div>
				<?php endwhile; ?>
			</div>
		</body>
	</html>
