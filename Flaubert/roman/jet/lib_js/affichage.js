// Librairie de fonctions d'affichage

var g_num_image = 0;

function aff_roll( lien, a_off, a_on, option )
{
	g_num_image += 1;
	s = '<a href="' + lien + '"';
	if( option ) s+= ' ' + option;
	s+= ' onMouseOut="aff_swapImgRestore()"'; 
	s+= ' onMouseOver="aff_swapImage(\'I' + g_num_image + '\',\'\',\'' + a_on + '\',1)"><img'; 
	s+= ' name="I' + g_num_image + '" border="0" src="' + a_off + '"></a>';

	document.write( s );
}


function aff_swapImgRestore() 
{
	var i,x,a=document.aff_sr; 
  for( i = 0; a && i < a.length && ( x = a[i] ) && x.oSrc; i++ ) x.src = x.oSrc;
}

function aff_preloadImages() 
{
	var d = document; 
	if( d.images )
	{ 
		if( ! d.aff_p ) d.aff_p = new Array();
    	var i, j = d.aff_p.length, a = aff_preloadImages.arguments; 
    	for( i = 0; i < a.length; i++ )
		{
    		if( a[i].indexOf( "#" ) != 0 )
    		{ 
    			d.aff_p[j] = new Image; 
    			d.aff_p[j++].src = a[i];
    		}
		}
   }
}

function aff_findObj( n, d )
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
  if( !x && d.getElementById ) x = d.getElementById( n ); 
  return x;
}

function aff_swapImage() 
{
 	var i, j = 0, x , a = aff_swapImage.arguments;
 	document.aff_sr = new Array; 
 	for( i = 0; i < ( a.length - 2 ); i += 3 )
 	{
 		if( ( x = aff_findObj( a[i] ) ) != null )
 		{ 
 			document.aff_sr[j++] = x;
 			if( ! x.oSrc ) x.oSrc = x.src;
 			x.src = a[i+2];
 		}
 	}
}

function aff_showHideLayers() 
{
  var i, p, v, obj, args = aff_showHideLayers.arguments;

	for( i = 0; i < ( args.length - 1 ); i += 2 )
  	{
  		if( ( obj = aff_findObj( args[ i ] ) ) != null ) 
  		{ 
  			v = args[ i + 1 ];
    		if( obj.style ) 
    		{ 
    			obj = obj.style; 
    			v = ( v == 'show' ) ? 'visible' : ( v = 'hide' ) ? 'hidden' : v; 
    		}
    		obj.visibility = v;
    	}
	}
}

	var lastScrollY = 0;

	NS = ( document.layers ) ? 1 : 0;
	IE = ( document.all ) ? 1: 0;
	NS7 = ( navigator.userAgent.indexOf( "Gecko" ) != -1 );

	function Colle( quoi ) 
	{
		if( IE ) diffY = document.body.scrollTop;
		if( NS || NS7 ) diffY = self.pageYOffset;
		if( diffY < 30 ) 
		{
			aff_showHideLayers( quoi, 'hide' );
		} else if( diffY != lastScrollY ) {
			aff_showHideLayers( quoi, 'show' );
  		if( NS7 && ( obj = aff_findObj( quoi ) ) != null ) { obj.style.top = diffY + 25; }
  		else 
  		{
				if( IE ) eval( 'document.all.' + quoi + '.style.pixelTop = diffY + 25;' );
				if( NS ) eval( 'document.' + quoi + '.top = diffY + 25;' );
			}
			lastScrollY = diffY;
		}
	}

	function place( quoi, x, y ) 
	{
  		if( NS7 && ( obj = aff_findObj( quoi ) ) != null ) { obj.style.top = x; obj.style.left = y; }
  		else 
  		{
			if( IE ) {
				eval( 'document.all.' + quoi + '.style.pixelTop = x;' );
				eval( 'document.all.' + quoi + '.style.pixelLeft = y;' );
			}
			if( NS ) {
				eval( 'document.' + quoi + '.top = x;' );
				eval( 'document.' + quoi + '.left = y;' );
			}
		}
		aff_showHideLayers( quoi, 'show' );
	}

	function jet_colle( lay_a_coller ) 
	{
		if( NS || IE || NS7 ) action = window.setInterval( "Colle( '" + lay_a_coller + "' )" , 100 );
	}
	
	function ajout_favoris( lien, texte )
	{
		window.external.AddFavorite( lien, texte);
	}