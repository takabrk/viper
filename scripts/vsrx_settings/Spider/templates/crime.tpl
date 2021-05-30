<style type="text/css" scoped>
    .infoWindow{
        font-size:10pt;
        background-color:#ff99ff;
        color:#ffffff;
        padding:15px;
        display:block;
    }
    .infotext{
        color:#000000;
    }
</style>
<div id="gmap" style="width:99%;height:370px;border:1px solid Gray;"></div><br/>
<input type="button" value="Click" onclick="markers()" /><br/>
<script type="text/javascript">
    var spots = [];
    {foreach $item1 as $itemdata1}
spots.push([{$itemdata1.lat},{$itemdata1.lng},'<p class="infotext">{$itemdata1.description|nl2br|strip:" "|auto_link}</p>']);
    {/foreach}
    console.log(spots);
</script>
<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"></script>
<script type="text/javascript">
    var mapObj = null;
    google.maps.event.addDomListener(window,"load",function(){
        var lat = 35.5949865;
        var lng = 139.5493209;
        var mapOptions = {
            zoom : 5,
            center : new google.maps.LatLng(lat,lng),
            mapTypeId : google.maps.MapTypeId.HYBRID,
            scaleControl : true
        }
        mapObj = new google.maps.Map(document.getElementById("gmap"),mapOptions);
        return mapObj;
    });
    var markers = function(){
        for(var i=0;i<spots.length;i++){
           var marker = new google.maps.Marker({
                position : new google.maps.LatLng(spots[i][0],spots[i][1]),
                map : mapObj
            });
            infowindow(marker,spots[i][2]);
        }
    }
    var infowindow = function(marker,description){
        google.maps.event.addListener(marker,"click",function(event){
            new google.maps.InfoWindow({
                content : description
            }).open(marker.getMap(),marker);
        });
    }
</script>
