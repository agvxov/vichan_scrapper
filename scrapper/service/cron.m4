define(NL, `
')dnl
define(`PWD', translit(esyscmd(`pwd'), NL))dnl
define(realpath, `translit(esyscmd(readlink -f $1), NL)')dnl
define(`ROOT', realpath(PWD`/../../'))dnl
0	*	* * *	root	make -C "ROOT" scrap
30	*/3 * * *	root	make -C "ROOT" repair
