<?php
	define('COLORS', [
				["#ff0000", "white"], /* Red */
				["#ffa500", "black"], /* Orange */
				["#ffff00", "black"], /* Yellow */
				["#00ff00", "black"], /* Lime */
				["#008000", "white"], /* Green */
				["#00ffff", "black"], /* Aquamarine */
				["#00bfff", "white"], /* Cyan */
				["#0000ff", "white"], /* Blue */
				["#4b0082", "white"], /* Indigo */
				["#ffc0cb", "black"], /* Pink */
				["#ff00ff", "black"], /* Magenta */
				["#ff7f50", "black"], /* Coral */
				["#fa8072", "white"], /* Salmon */
				["#ff6347", "white"], /* Tomato */
				["#ffd700", "black"], /* Gold */
				["#f0e68c", "black"], /* Khaki */
				["#d2b48c", "white"], /* Tan */
				["#d2691e", "white"], /* Chocolate */
				["#a0522d", "white"], /* Sienna */
				["#800000", "white"], /* Maroon */
				["#808080", "white"], /* Gray */
				["#000000", "white"], /* Black */
				["#ffffff", "black"] /* White */
	]);

	function ids2color($id){
			return $id == 'ONION' ? ["#800080", "white"] /* Purple */ : COLORS[intval(crc32($id)) % 23];
	}
?>
