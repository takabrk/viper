<?php /* Smarty version 3.1.24, created on 2017-09-12 13:24:09
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/crime.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:50174248959b76169d27fd6_18323775%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '369e01e151e8b189a6713759a14f342c1b41544b' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/crime.tpl',
      1 => 1504758084,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '50174248959b76169d27fd6_18323775',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b76169d46018_91893242',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b76169d46018_91893242')) {
function content_59b76169d46018_91893242 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '50174248959b76169d27fd6_18323775';
?>
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
<?php echo '<script'; ?>
 type="text/javascript">
    var spots = [];
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
spots.push([<?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['lat'];?>
,<?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['lng'];?>
,'<p class="infotext"><?php echo smarty_modifier_auto_link(preg_replace('!\s+!u', " ",nl2br($_smarty_tpl->tpl_vars['itemdata1']->value['description'])));?>
</p>']);
    <?php
$_smarty_tpl->tpl_vars['itemdata1'] = $foreach_itemdata1_Sav;
}
?>
    console.log(spots);
<?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&key=AIzaSyAWv_TnaP8NnX_SzE2suIecRubjaIf-Rus"><?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 type="text/javascript">
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
<?php echo '</script'; ?>
>
<?php }
}
?>