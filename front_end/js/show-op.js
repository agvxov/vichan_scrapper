/*
 * show-op
 * https://github.com/savetheinternet/Tinyboard/blob/master/js/show-op.js
 *
 * Adds "(OP)" to >>X links when the OP is quoted.
 *
 * Released under the MIT license
 * Copyright (c) 2012 Michael Save <savetheinternet@tinyboard.org>
 * Copyright (c) 2014 Marcin Łabanowski <marcin@6irc.net>
 *
 * Usage:
 *   $config['additional_javascript'][] = 'js/jquery.min.js';
 *   $config['additional_javascript'][] = 'js/show-op.js';
 *
 */

$(document).ready(function(){
	let OP = parseInt($('.op .post_no').text().replace(/^\D+/g, ""))
	if(isNaN(OP)){ return; }

	var showOPLinks = function() {
		$(this).find('div.post_body a:not([rel="nofollow"])').each(function() {
			var postID;
			
			if(postID = $(this).text().match(/^>>(\d+)$/))
				postID = postID[1];
			else
				return;
			
			if (postID == OP) {
				$(this).after(' <small>(OP)</small>');
			}
		});
	};
	
	$('div.post.reply').each(showOPLinks);
});



