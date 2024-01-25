<!DOCTYPE html>
	<html>
		<?php
			require_once('global.php');
			require_once('config.php');

			# Query validation
			if(!isset($_GET['page'])){
				$page = 1;
			}else{
				$page = intval($_GET['page']);
			}
			if(validate_board_name($_GET['board'])){
				$board = $_GET['board'];
			}else{
				header('Location: /404.php');
				die();
			}
		?>
		<head>
			<title>Examplechan - Archive /<?=$board?>/</title>
			<link rel="stylesheet" href="global.css">
			<meta charset="utf-8">
			<style>
				span {
					color: #06df20;
				}

				.thread {
					box-sizing: border-box;
					padding: 20px;
				}
				.thread:hover {
					background: teal;
					cursor: pointer;
				}
				.thread img {
					width: 200px;
				}
				.file {
					max-height: 400px;
					overflow-y: hidden;
				}
				.page_list {
					text-align: center;
					font-size: 2rem;
					color: yellow;
					font-weight: bold;
				}
					.page_list a:link {
						color: lime;
						font-weight: normal;
					}
					.page_list a:visited {
						color: lightgreen;
					}
			</style>
		</head>
		<body>
			<div id=body_main>
				<div id=index_header>
					<p>Examplechan Archive - /<?=$board?>/</p>
					<a href="/">
						<img id=plant src="media/plant.png" alt="fc_logo"></img>
					</a>
				</div>
				<div class=page_list>
					[
					<?php
						$post_count = $db->querySingle('SELECT COUNT(*) count FROM posts WHERE board = \'/' . $_GET['board'] . '/\' and thread is NULL;');
						$page_count = ceil($post_count / $config['posts_per_page']);
						for($i = 0; $i < $page_count; $i++):
					?>
						<a href="/board.php?board=<?=$board?>&page=<?=$i+1?>"><?=$i+1?></a>
					<?php
						endfor;
					?>
					]
				</div>
				<hr>
				<hr>
				<?php
					$query = 'SELECT * FROM posts WHERE ' .
									'board = \'/' . $board . '/\' ' .
										'AND ' .
									'thread IS NULL ' .
									'ORDER BY id DESC ' .
									'LIMIT ' . $config['posts_per_page'] . ' ' .
									'OFFSET ' . ($config['posts_per_page']*($page-1)) . ';';
					$results = $db->query($query);

					while($row = $results->fetchArray()):
				?>
					<div class="thread" onclick="window.location='/post.php?board=<?=$board?>&post=<?=$row['id']?>';">
						<div>
							<?=print_post_head($row)?>
							<div class='files'>
								<?=print_files($row['id'], $row['board'])?>
							</div>
							<div class='post_body'>
								<?=$row['body']?>
							</div>
						</div>
					</div>
					<hr>
				<?php endwhile; ?>
				<script id=page_list_duplicator type="text/javascript" src="js/duplicate_page_list.js"></script>
			</div>
		</body>
	</html>
