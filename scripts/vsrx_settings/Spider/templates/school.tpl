   <style type="text/css" scoped>
        .infoWindow{
            font-size:10px;
            background-color:#ff99ff;
            color:#ffffff;
            padding:15px;
            display:block;
        }
  </style>
    <div id="gmap2" style="width:99%;height:370px;border:1px solid Gray;"></div><br/>
    <select id="jkmaps"  onChange="selectChange2()">
        <option value="base">項目を選んで下さい</option>
           {foreach $item1 as $itemdata1}
           <option value="{$itemdata1.id}">{$itemdata1.name}</option>
           {/foreach}
    </select> |
    <input type="button" value="Satellite Mode2" onclick="changeSatellite2()"/> |
    <input type="button" value="Roadmap Mode2" onclick="changeRoadmap2()"/>
    <h1>ドライブルート</h1>
  Point A : <input id="address1" type="text" /> |  Point B : <input id="address2" type="text" /><input type="button" value="Geocoder" onclick="dg()" />

<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"></script>
<script type="text/javascript">
    var mapObj = null;
    google.maps.event.addDomListener(window,"load",function(){
        var lat = 35.6809691281986;
        var lng = 139.7668620944023;
        var mapOptions = {
            zoom : 18,
            center : new google.maps.LatLng(lat,lng),
            mapTypeId : google.maps.MapTypeId.HYBRID,
            scaleControl : true
        }
        mapObj = new google.maps.Map(document.getElementById("gmap2"),mapOptions);
        return mapObj;
    });
    var dg = function(){
        var request = {
            origin : $("#address1").val(),
            destination : $("#address2").val(),
            travelMode : google.maps.DirectionsTravelMode.DRIVING,
            provideRouteAlternatives : true
        };
        var directionsService = new google.maps.DirectionsService();
        directionsService.route(request,function(result,status){
            if(status == google.maps.DirectionsStatus.OK){
                for(var routeIndex = 0;routeIndex < result.routes.length;routeIndex++){
	            var directionsRenderer = new google.maps.DirectionsRenderer();
	            directionsRenderer.setDirections(result);
	            directionsRenderer.setRouteIndex(routeIndex);
	            directionsRenderer.setMap(mapObj);
	        }
            }
        });
    }
    var changeSatellite2 = function(){
        mapObj.setMapTypeId(google.maps.MapTypeId.HYBRID);
    }
    var changeRoadmap2 = function(){
        mapObj.setMapTypeId(google.maps.MapTypeId.ROADMAP);
    }
    var selectChange2 = function(){
        var sl = document.getElementById("jkmaps");
        var value = sl.options[sl.selectedIndex].value;
        var sci2 = function(schoolId,schoolName,schoolAddress){
            if(value == schoolId){
                request = {
                    address : schoolAddress
                }
                html = "<div class='infoWindow'>"+schoolName+"</div>";
            }
        }
        {foreach $item2 as $itemdata2}
        sci2('{$itemdata2["id"]}','{$itemdata2["name"]}','{$itemdata2["address"]}');
        {/foreach}
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode(request,function(results,status){
        if(status == google.maps.GeocoderStatus.OK){
            var location = results[0].geometry.location;
            var marker = new google.maps.Marker({
                position : location,
                title : request.address,
                map : mapObj
            });
            mapObj.panTo(location);
            google.maps.event.addListener(marker,"click",function(){
                var infoWindow = new google.maps.InfoWindow();
                infoWindow.setContent(html);
                infoWindow.open(mapObj,marker);
            });
        }
    });
}
</script>
