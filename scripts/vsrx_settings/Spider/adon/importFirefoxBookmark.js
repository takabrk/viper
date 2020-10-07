function importFirefoxBookmarks(id,x,y){
	var bm_root = bookmarks.children[0];
	var bma = [];
	for(var i=2;i<20;i++){
		bma.push(bm_root.children[i]);
	}
	var bmb = [];
	for(var i=0;i<bma[x].children.length;i++){
		bmb.push(bma[x].children[i]);
	}
	var bmc = [];
	for(var i=0;i<bmb[y].children.length;i++){
		bmc.push(bmb[y].children[i]);
	}
	for(var i=0;i<bmc.length;i++){
		$d[getid](id)[ih] += bmc[i].title + "<br />"
				 + '<a href="' + bmc[i].uri + '" target="_blank">' + bmc[i].uri + '</a><br />';
	}
}
