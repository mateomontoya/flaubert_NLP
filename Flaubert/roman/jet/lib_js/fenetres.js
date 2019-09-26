// Fenetres pop_up

var InternetExplorer = navigator.appName.indexOf("Microsoft") != -1;
var Netscape = ( navigator.appName == "Netscape" );
var MSWin = navigator.userAgent.indexOf("Win") != -1;
var ref_w_choix = null
var ref_w_choix2 = null
var ref_w_image = null
var num_fen_upload = 0

function fen_findObj( n, d )
{
 	var p, i, x;  
 	if( ! d ) d = document; 
 	if( ( p = n.indexOf( "?" ) ) > 0 && parent.frames.length )
 	{
    	d = parent.frames[ n.substring( p+1 ) ].document; 
    	n = n.substring( 0, p );
 	}
  if( ! ( x = d[n] ) && d.all ) x = d.all[n];
  for( i = 0; ! x && i < d.forms.length; i++ ) x = d.forms[i][n];
  for( i = 0; ! x && d.layers && i < d.layers.length; i++ ) x = aff_findObj( n, d.layers[i].document);
  if( ! x && d.getElementById ) x = d.getElementById( n ); 
  return x;
}

function ouvre_fen_flv( url, w, h, l, t, nom )
{
	if( InternetExplorer && ref_w_choix ) ref_w_choix.close();
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = 20; if( ! t ) t = 20;
	if( ! nom ) nom = "w";
	ref_w_choix = window.open( url, nom, 'toolsbar=0,scrollbars=0,resizable=0,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t );
	ref_w_choix.focus();
}

function ouvre_fen_upload( url, w, h, l, t, nom )
{
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = 20; if( ! t ) t = 20;
	window.open( url, nom, 'toolsbar=0,scrollbars=0,resizable=0,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t );
}

function ouvre_fen_zoom_texte( formulaire, titre, champs, w, h, l, t )
{
	if( ! w ) w = 500; if( ! h ) h = 600;
	if( ! l ) l = ( screen.width - w ) / 2; 
	if( ! t ) t = ( screen.height - h ) / 2;

	obj = fen_findObj( champs );
	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();
	
	ref_w_choix = window.open( "", "w_texte", 'width=' + w + ',height=' + h + ',left=' + l + ',top=' + t + ', scrollbars=no, toolbar=no, status=no' );
	r = ref_w_choix.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' );
	r.write( '<link rel=stylesheet href="../admin.css">' );
	r.write( '</head><body class=bodycentre><form name=f method=post><div align=center>' );
	r.write( '<table width="90%" heigth="100%" border=0 cellpadding=2 cellspacing=2>' );
	r.write( '<tr><td width="50%"></td><td width="50%"></td></tr>' );
	r.write( '<tr><td colspan=2 class=c><textarea cols=60 rows=35 wrap=soft name=t>' );
	r.write( obj.value );
	r.write( '</textarea></td></tr><tr><td>&nbsp;</td></tr>' );
	r.write( '<tr><td><input type=button value="VALIDER" onClick="window.opener.document.' + formulaire + '.' + champs + '.value=document.f.t.value; window.opener.document.' + formulaire + '.submit(); self.close();" ></td>' );
	r.write( '<td class=d><input type=button value="ANNULER" onClick="' );
	r.write( 'self.close();"></td>' );
	r.write( '</tr><tr><td>&nbsp;</td></tr></table>' );
	r.write( '</div></form></body></html>' );
	ref_w_choix.focus()
}

function ouvre_fen_photo( fich, w, h, titre, legende, l, t )
{
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = ( screen.width - w ) / 2; 
	if( ! t ) t = ( screen.height - h ) / 2;
	if( ! titre ) titre = 'Image';

	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();

	ref_w_choix = window.open( "", titre, 'width=' + w + ',height=' + h + ',left=' + l + ',top=' + t + ',toolbar=no,location=0,directories=no,menubar=0,resizable=0,scrollbars=no,status=no' );
	r = ref_w_choix.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' )
	r.write( '<style type="text/css">body { margin-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; }</style>' )
	r.write( '</head><body bgcolor="#000040" onBlur="self.close()" text="#003300">' )
	if( legende ) {
		r.write( '<table bgcolor="#000011" align=center valign=center border=0 cellpadding=0 cellspacing=0><tr valign="bottom">' )
		r.write( '<td width=' + w + ' height=' + h + ' align=right background="' + fich + '">' )
		r.write( '<font color="#000000" face="Arial, Helvetica, sans-serif" size="2">' + legende + '&nbsp;</font></td></tr></table>' )
	} else {
		r.write( '<img src="' + fich + '" width=' + w + ' height=' + h + '>' )
	}
	r.write( '</body></html>' )

	ref_w_choix.focus()
}

function ouvre_fen_image( fich, largeur, hauteur, titre )
{
	if( InternetExplorer && MSWin && ref_w_image ) ref_w_image.close();

	ref_w_image = window.open( "", titre, 'width=' + largeur + ',height=' + hauteur  +  ',toolbar=no,location=0,directories=no,menubar=0,resizable=0,scrollbars=no,status=no' )
	r = ref_w_image.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' )
	r.write( '<style type="text/css">body { margin-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px;}</style>' )
	r.write( '</head><body bgcolor="#000040" onBlur="self.close()">' )
	r.write( '<body><img src="' + fich + '" width=' + largeur + ' height=' + hauteur + '></body></html>' )

	ref_w_image.focus()
}

function ouvre_fen_texte( titre, texte, w, h, l, t )
{	
	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();

	if( ! w ) w = 400; if( ! h ) h = 200;
	if( ! l ) l = ( screen.width - w ) / 2; 
	if( ! t ) t = ( screen.height - h ) / 2;
	if( ! titre ) titre = 'Image';
	
	ref_w_choix = window.open( "", "w_valide", 'width=' + w + ', height=' + h + ', left=' + l + ',top=' + t + ', scrollbars=no, toolbar=no, status=no' );
	r = ref_w_choix.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' );
	r.write( '</head><body onBlur="self.close()"><form name=f method=post><div align=center>' );
	r.write( '<table width="95%" heigth="100%" border=0 cellpadding=5 cellspacing=5 align=center>' );
	r.write( '<tr><td>' + texte + '</td></tr>' );
	r.write( '<tr><td align=center><input type=button value="OK" onClick="self.close();"></td></tr>' );
	r.write( '</div></form></body></html>' );
	ref_w_choix.focus();		
}

function ouvre_fen_validation( titre, texte, oui, non )
{
	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();

	l = ( screen.width - 400 ) / 2;
	t = ( screen.height - 200 ) / 2;
	
	ref_w_choix = window.open( "", "w_valide", 'width=400, height=200, left=' + l + ',top=' + t + ', scrollbars=no, toolbar=no, status=no' );
	r = ref_w_choix.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' );
	r.write( '<link rel=stylesheet href="style.css">' );
	r.write( '</head><body class=bodycentre onBlur="self.close()"><form name=f method=post><div align=center>' );
	r.write( '<table width="80%" heigth="100%" border=0 cellpadding=5 cellspacing=5>' );
	r.write( '<tr><td width="50%"></td><td width="50%"></td></tr>' );
	r.write( '<tr><td colspan=2>' + texte + '</td></tr><tr><td>&nbsp;</td></tr>' );
	r.write( '<tr><td><input type=button value="OK" onClick="window.opener.location.href=\'' + oui + '\'; self.close();" ></td>' );
	r.write( '<td align=center><input type=button value="CANCEL" onClick="' );
	if( non ) r.write( 'window.opener.location.href=\'' + non + '\'; ' );  
	r.write( 'self.close();"></td>' );
	r.write( '</tr><tr><td>&nbsp;</td></tr></table>' );
	r.write( '</div></form></body></html>' );
	ref_w_choix.focus()
}

function valide_submit( formulaire, titre, texte, f_css, nom_hidden, w, h, l, t )
{
	if( ! w ) w = 300; if( ! h ) h = 150;
	if( ! l ) l = ( screen.width - w ) / 2; 
	if( ! t ) t = ( screen.height - h ) / 2;
	
	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();
	
	ref_w_choix = window.open( "", "w_valide", 'width=' + w + ', height=' + h + ', left=' + l + ',top=' + t + ', scrollbars=no, toolbar=no, status=no' );
	r = ref_w_choix.document
	r.open();
	r.write( '<html><head><title>' + titre + '</title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">' );
	if( f_css ) t = f_css; else t = "../admin.css";
	r.write( '<link rel=stylesheet href="' + t + '">' );
	r.write( '</head><body onBlur="self.close()"><form name=f method=post><div align=center>' );
	r.write( '<table width=100% heigth="100%" width=100%border=0 cellpadding=5 cellspacing=5>' );
	r.write( '<tr><td width="50%"></td><td width="50%"></td></tr>' );
	r.write( '<tr><td colspan=2>' + texte + '</td></tr><tr><td>&nbsp;</td></tr>' );
	r.write( '<tr><td class=c><input type=button class=bouton value="VALIDER" onClick="' );
	if( nom_hidden ) r.write( 'window.opener.' + formulaire + '.' + nom_hidden + '.value=\'OUI\'; ' );
	r.write( 'window.opener.' + formulaire + '.submit(); self.close();" ></td>' );
	r.write( '<td class=c><input type=button class=bouton value="ANNULER" onClick="' );
	r.write( 'self.close();"></td>' );
	r.write( '</tr><tr><td>&nbsp;</td></tr></table>' );
	r.write( '</div></form></body></html>' );
	ref_w_choix.focus()
}


function ouvre_fen_depart( url, w, h, l, t )
{
	if( InternetExplorer && ref_w_choix ) ref_w_choix.close();
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = 20; if( ! t ) t = 20;
	ref_w_choix = window.open( url, "d", 'scrollbars=no,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t );
	ref_w_choix.focus();
}

function ouvre_fen_info( url, w, h, l, t, nom )
{
	if( InternetExplorer && ref_w_choix ) ref_w_choix.close();
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = 20; if( ! t ) t = 20;
	if( ! nom ) nom = "w";
	ref_w_choix = window.open( url, nom, 'toolsbar=0,scrollbars=1,resizable=1,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t );
	ref_w_choix.focus();
}

function ouvre_fen_info2( url, w, h, l, t )
{
	if( InternetExplorer && ref_w_choix2 ) ref_w_choix2.close();
	if( ! w ) w = 300; if( ! h ) h = 400;
	if( ! l ) l = 20; if( ! t ) t = 20;
	ref_w_choix2 = window.open( url, "w2", 'toolsbar=0,scrollbars=1,resizable=1,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t );
	ref_w_choix2.focus();
}

function plein_ecran( url )
{
	if( InternetExplorer && MSWin && ref_w_choix ) ref_w_choix.close();
	
	w = screen.width;
	h = screen.height;

	if( InternetExplorer && MSWin ) { // IE Windows
		ref_w_choix = window.open( url, "w", "fullscreen,scrollbars" ); 
	} else if( ! InternetExplorer && MSWin ) { // NS Windows
		ref_w_choix = window.open( url, "w", "outerwidth=" + w + ",outerheight=" + h + ",top=0,left=0" );
	} else if( InternetExplorer && ! MSWin ) { // IE Mac
		ref_w_choix = window.open( url, "w", "width=" + w + ",height=" + h + ",top=0,left=0,scrollbars=no" );
	} else if( ! InternetExplorer && ! MSWin ) { // NS Mac
		ref_w_choix = window.open( url, "w", "width=" + ( w - 10 ) + ",height=" + ( h - 50 ) + ",top=0,left=0" );
	}

	ref_w_choix.focus();
}