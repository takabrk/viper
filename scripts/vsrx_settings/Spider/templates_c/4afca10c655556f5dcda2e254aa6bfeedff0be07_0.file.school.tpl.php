<?php /* Smarty version 3.1.24, created on 2017-09-14 18:47:41
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:65666918859ba503d868c61_78966552%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '4afca10c655556f5dcda2e254aa6bfeedff0be07' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school.tpl',
      1 => 1504800453,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '65666918859ba503d868c61_78966552',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
    'item2' => 0,
    'itemdata2' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59ba503d8a91a9_75862904',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59ba503d8a91a9_75862904')) {
function content_59ba503d8a91a9_75862904 ($_smarty_tpl) {

$_smarty_tpl->properties['nocache_hash'] = '65666918859ba503d868c61_78966552';
?>
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
           <?php
$_from = $_smarty_tpl->tpl_vars['item1']->value;
if (!is_array($_from) && !is_object($_from)) {
settype($_from, 'array');
}
$_smarty_tpl->tpl_vars['itemdata1'] = new Smarty_Variable;
$_smarty_tpl->tpl_vars['itemdata1']->_loop = false;
foreach ($_from as $_smarty_tpl->tpl_vars['itemdata1']->value) {
$_smarty_tpl->tpl_vars['itemdata1']->_loop = true;
$foreach_itemdata1_Sav = $_smarty_tpl->tpl_vars['itemdata1'];
?>
           <option value="<?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['id'];?>
"><?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['name'];?>
</option>
           <?php
$_smarty_tpl->tpl_vars['itemdata1'] = $foreach_itemdata1_Sav;
}
?>
    </select> |
    <input type="button" value="Satellite Mode2" onclick="changeSatellite2()"/> |
    <input type="button" value="Roadmap Mode2" onclick="changeRoadmap2()"/>
    <h1>ドライブルート</h1>
  Point A : <input id="address1" type="text" /> |  Point B : <input id="address2" type="text" /><input type="button" value="Geocoder" onclick="dg()" />

<?php echo '<script'; ?>
 type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"><?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 type="text/javascript">
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
        <?php
$_from = $_smarty_tpl->tpl_vars['item2']->value;
if (!is_array($_from) && !is_object($_from)) {
settype($_from, 'array');
}
$_smarty_tpl->tpl_vars['itemdata2'] = new Smarty_Variable;
$_smarty_tpl->tpl_vars['itemdata2']->_loop = false;
foreach ($_from as $_smarty_tpl->tpl_vars['itemdata2']->value) {
$_smarty_tpl->tpl_vars['itemdata2']->_loop = true;
$foreach_itemdata2_Sav = $_smarty_tpl->tpl_vars['itemdata2'];
?>
        sci2('<?php echo $_smarty_tpl->tpl_vars['itemdata2']->value["id"];?>
','<?php echo $_smarty_tpl->tpl_vars['itemdata2']->value["name"];?>
','<?php echo $_smarty_tpl->tpl_vars['itemdata2']->value["address"];?>
');
        <?php
$_smarty_tpl->tpl_vars['itemdata2'] = $foreach_itemdata2_Sav;
}
?>
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
<?php echo '</script'; ?>
>
<?php }
}
?>