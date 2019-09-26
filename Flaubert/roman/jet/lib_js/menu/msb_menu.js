// appelée à l'ouverture d'un menu
// codemenus est un tableau qui contient les codes de chgt d'images dans la page
function menushow(num,pnum,inum)
{
	var images = document.getElementById("imgs");
	var legende = document.getElementById("legende");
	var declimage = ''; // image declinaison

	if( images != null && codemenus[ num ].length > 1 )
	{
		if( codemenus[ num ].length > 1 ) declimage = "/dossiers/decli/" + codemenus[ num ];
		else legende.innerHTML = '';
		
		if (declimage != '')
		{
			shtml = '<img src="' + g_base_web + declimage + '" width="614" height="330" class="decli">';
			shtml += '<img src="' + g_base_web + '/dossiers/decli/trame.jpg" width="614" height="105" class="trame">';
			shtml += '<img src="' + g_base_web + '/dossiers/decli/corne2.gif" width="142" height="186" class="corne">';
			images.innerHTML = shtml;
			legende.innerHTML = '';
			for (var nom in legendes)
			{
				if (nom == codemenus[num])
				{
					legende.innerHTML = legendes[nom];
					break;
				}
			}
		}
		else images.innerHTML = '';
	}
	var menu1 = document.getElementById("menu1");
	var menu2 = document.getElementById("menu2");
	if (menu1 != null)
	{
		if ((affa[num] != '')&&(affa[num] != '-'))
			menu1.innerHTML = affa[num]+'&nbsp;<img src="' + g_base_web + 'images/visu/ico_flb1.gif" width="14" height="7" align="absmiddle">';
		else
			menu1.innerHTML = '';
	}
	if (menu2 != null)
	{
		if ((affb[num] != '')&&(affb[num] != '-'))
			menu2.innerHTML = affb[num]+'&nbsp;<img src="' + g_base_web + 'images/visu/ico_flb1.gif" width="14" height="7" align="absmiddle">';
		else
			menu2.innerHTML = '';
	}
}