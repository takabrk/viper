   <style type="text/css" scoped>
        .baselayer{
            width:100%;
            height:800px;
            margin:auto 0;
            padding:0;
        }
        .infoWindow{
            font-size:10px;
            background-color:#ff99ff;
            color:#ffffff;
            padding:15px;
            display:block;
        }
        .maps{
            width:100%;
            height:370px;
            margin:0;
            padding:0;
        }
        .bottomlayer{
            width:500px;
            height:370px;
            margin:0;
            padding:0;
        }
        .selectlayer{
            float:left;
        }
        #gmap3{
            float:left;
            width:50%;
            height:370px;
            border:1px solid Gray;
        }
        #streetview_canvas{
            float:right;
            width:40%;
            height:370px;
            background-color:#000000;
        }
  </style>
   <div class="baselayer">
    <div class="maps">
        <div id="gmap3"></div>
        <div id="streetview_canvas"></div>
    </div>
    <div class="bottomlayer">
    <select id="itmaps"  onchange="selectChange3()">
        <option value="base">項目を選んで下さい</option>
           {foreach $item1 as $itemdata1}
           <option value="{$itemdata1.id}">{$itemdata1.name}</option>
           {/foreach}
    </select> |
    <input type="button" value="Satellite Mode3" onclick="changeSatellite3()"/> |
    <input type="button" value="Roadmap Mode3" onclick="changeRoadmap3()"/>
    </div>
    </div>
<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"></script>
<script type="text/javascript">
  var mapObj = null;
  function initialize(){
      var lat = 35.6809691281986;
      var lng = 139.7668620944023;
      var mapOptions = {
          zoom : 18,
          center : new google.maps.LatLng(lat,lng),
          mapTypeId : google.maps.MapTypeId.HYBRID,
          scaleControl : true
      }
      mapObj = new google.maps.Map(document.getElementById("gmap3"),mapOptions);
  }
      var changeSatellite3 = function(){
           mapObj.setMapTypeId(google.maps.MapTypeId.HYBRID);
      }
      var changeRoadmap3 = function(){
           mapObj.setMapTypeId(google.maps.MapTypeId.ROADMAP);
      }
      var selectChange3 = function(){
           var sl = document.getElementById("itmaps");
           var value = sl.options[sl.selectedIndex].value;
           var sci3 = function(schoolId,schoolName,schoolAddress){
               if(value == schoolId){
                   request = {
                      address : schoolAddress
                   }
                   html = "<div class='infoWindow'>"+schoolName+"</div>";
               }
           }
         {foreach $item2 as $itemdata2}
        sci3('{$itemdata2["id"]}','{$itemdata2["name"]}','{$itemdata2["address"]}');
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
	           var streetviewdiv = document.getElementById("streetview_canvas");
	           var streetviewOptions = {
	               position : location
	           }
	           var streetview = new google.maps.StreetViewPanorama(streetviewdiv,streetviewOptions);
	           mapObj.setStreetView(streetview);
	           mapObj.bindTo("center",streetview,"position");
	           google.maps.event.addListener(marker,"click",function(){
                       var infoWindow = new google.maps.InfoWindow();
                       infoWindow.setContent(html);
                       infoWindow.open(mapObj,marker);
                   });
                }
	   });
      }
google.maps.event.addDomListener(window,"load",initialize);
</script>
