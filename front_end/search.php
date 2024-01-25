<!DOCTYPE html>
	<html>
		<?php
			require_once('config.php');
		?>
		<head>
			<title>Examplechan - Archive</title>
			<link rel="stylesheet" href="global.css">
			<meta charset="utf-8">
			<style>
			</style>
		</head>
		<body>
			<div id=body_main>
				<div id=index_header>
					<p>Examplechan Archive - Advanced Search</p>
					<div>
						<?php
							if(!$config['search_enabled']){
								echo "<h3>Advanced search was disabled on this instance due to securitiy reasons. It recommended you get a local copy and search that way.</h3>";
								die();
							}
						?>
					</div>
				</div>
				<div id=search_box>
				</div>
				<div id=result_box>
				</div>
			</div>
			<script>
			</script>
		</body>
	</html>
