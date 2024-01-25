<!DOCTYPE html>
	<html>
		<?php
			require_once('config.php');
		?>
		<head>
			<title>ViChan - Archive</title>
			<link rel="stylesheet" href="global.css">
			<meta charset="utf-8">
			<style>
				button {
					float: left;
					height: 100%;
					width: 100%;
					color: green;
					font-weight: bold;
					font-size: 2.4rem;
				}

				a {
					display: inline-block;
					height: 100%;
					width: 100%;
				}

				.bdiv {
					height: 100px;
					width: 300px;
				}

				#mid {
					display: flex;
					justify-content: space-evenly;
					padding-top: 40px;
				}
			</style>
		</head>
		<body>
			<div id=body_main>
				<div id=index_header>
					<p>Vichan Archive - Memetic core</p>
				</div>
				<hr>
				<hr>
				<div id=mid>
					<div class=bdiv>
						<a href="vichan_archive_data.tar.gz" download>
							<button class=flashy_button>
								Database + Files
							</button>
						</a>
					</div>
					<div class=bdiv>
						<a href="vichan_archive.tar.gz" download>
							<button class=flashy_button>
								Scrapper + Front end
							</button>
						</a>
					</div>
				</div>
			</div>
			<script>
			</script>
		</body>
	</html>
