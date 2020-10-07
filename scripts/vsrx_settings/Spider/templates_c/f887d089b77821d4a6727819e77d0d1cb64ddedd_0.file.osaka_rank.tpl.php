<?php /* Smarty version 3.1.24, created on 2017-09-08 20:12:05
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/osaka_rank.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:198619833259b27b05d83266_33617084%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'f887d089b77821d4a6727819e77d0d1cb64ddedd' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/osaka_rank.tpl',
      1 => 1504869071,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '198619833259b27b05d83266_33617084',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b27b05d87096_54799832',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b27b05d87096_54799832')) {
function content_59b27b05d87096_54799832 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '198619833259b27b05d83266_33617084';
?>
<h2>大阪の地域別総合力ランキング 2018</h2>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">地域名</th><th class="des">説明</th></tr>
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
        <tr class="tre"><td class="uni1"><?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['id'];?>
</td><td class="uni2"><?php echo $_smarty_tpl->tpl_vars['itemdata1']->value['name'];?>
</td><td class="des"><?php echo smarty_modifier_auto_link(preg_replace('!\s+!u', " ",nl2br($_smarty_tpl->tpl_vars['itemdata1']->value['description'])));?>
</td></tr>
    <?php
$_smarty_tpl->tpl_vars['itemdata1'] = $foreach_itemdata1_Sav;
}
?>
</table>
<?php }
}
?>