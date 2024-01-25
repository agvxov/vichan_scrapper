<!DOCTYPE html>
	<html>
		<?php
			require_once('global.php');
		?>
		<head>
			<title>ExampleChan - Archive</title>
			<link rel="stylesheet" href="global.css">
			<meta charset="utf-8">
			<style>
				#menu {
					display: flex;
					justify-content: space-between;
					gap: 0.5%;
				}
					#menu * {
						width: 100%;
						height: 30px;
						box-sizing: border-box
					}
				/* ------- */
				table {
					color: white;
					border: var(--std-border);
					width: 100%;
					border-collapse: collapse;
				}
					.hr {
						background: rgba(0, 128, 128, 0.5);
					}
					.hr:hover {
						background: forestgreen;
						cursor: pointer;
						/*font-weight: bold;*/
					}
					th, td {
						text-align: left;
					}
					th {
						color: lime;
						border: solid green 1px;
						border-collapse: collapse;
					}
					td {
						padding-left: 1%;
					}

			</style>
		</head>
		<body>
			<div id=body_main>
				<div id=index_header>
					<p>Examplechan Archive</p>
					<img id="plant" src="media/plant.png" alt="fc_logo"></img>
				</div>
				<div id=menu>
					<a href="/downloads.php">
						<button class=flashy_button>
							Get a copy
						</button>
					</a>
					<a href="/search.php">
						<button class=flashy_button>
							Advanced search
						</button>
					</a>
				</div>
				<hr>
				<table id=board_list>
					<thead>
						<tr class="hr">
							<th>Board</th>
							<th>Threads</th>
							<th>Files</th>
							<th>Posts</th>
						</tr>
					</thead>
					<tbody>
						<?php
							$results = $db->query('SELECT * FROM boards;');

							while($row = $results->fetchArray()):
						?>
							<tr class="hr" onclick="window.location='<?='/board.php?board='.trim($row['name'], '/')?>';">
								<td><?=$row['name']?> - <?=$row['desc']?></td>
								<td><?=$db->querySingle('SELECT COUNT(*) count FROM posts WHERE board = \'' . $row['name'] . '\' AND thread IS NULL;')?></td>
								<td><?=$db->querySingle('SELECT COUNT(*) FROM posts INNER JOIN files ON posts.id = files.post and posts.board = files.board WHERE posts.board = \'' . $row['name'] . '\';')?></td>
								<td><?=$db->querySingle('SELECT COUNT(*) count FROM posts WHERE board = \'' . $row['name'] . '\';')?></td>
							</tr>
						<?php endwhile; ?>
					</tbody>
				</table>
			</div>
			<script>
			</script>
		</body>
	</html>

