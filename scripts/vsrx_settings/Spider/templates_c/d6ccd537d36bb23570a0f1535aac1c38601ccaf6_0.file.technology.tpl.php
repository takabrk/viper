<?php /* Smarty version 3.1.24, created on 2017-09-14 18:47:50
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/technology.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:129344579959ba5046f0fb90_05142920%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'd6ccd537d36bb23570a0f1535aac1c38601ccaf6' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/technology.tpl',
      1 => 1504234588,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '129344579959ba5046f0fb90_05142920',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
    'item2' => 0,
    'itemdata2' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59ba5046f395a5_24575381',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59ba5046f395a5_24575381')) {
function content_59ba5046f395a5_24575381 ($_smarty_tpl) {

$_smarty_tpl->properties['nocache_hash'] = '129344579959ba5046f0fb90_05142920';
?>
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
    <input type="button" value="Satellite Mode3" onclick="changeSatellite3()"/> |
    <input type="button" value="Roadmap Mode3" onclick="changeRoadmap3()"/>
    </div>
    </div>
<?php echo '<script'; ?>
 type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"><?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 type="text/javascript">
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
        sci3('<?php echo $_smarty_tpl->tpl_vars['itemdata2']->value["id"];?>
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
<?php echo '</script'; ?>
>
<?php }
}
?>