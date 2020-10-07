<?php /* Smarty version 3.1.24, created on 2017-09-08 20:12:05
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/tv.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:7571370059b27b05d16827_52213424%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '8b9f0aaa1a9b89684a52029465196f9add689fad' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/tv.tpl',
      1 => 1504233609,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '7571370059b27b05d16827_52213424',
  'variables' => 
  array (
    'item2' => 0,
    'itemdata2' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b27b05d1caf0_01281932',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b27b05d1caf0_01281932')) {
function content_59b27b05d1caf0_01281932 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '7571370059b27b05d16827_52213424';
?>
    <h2>TV GUIDE</h2>
<table class="anp">
    <tr class="tre"><th class="uni2">サイト名</th><th class="des">URL</th></tr>
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
        <tr class="tre"><td class="uni2"><?php echo $_smarty_tpl->tpl_vars['itemdata2']->value['name'];?>
</td><td class="des"><?php echo smarty_modifier_auto_link(preg_replace('!\s+!u', " ",nl2br($_smarty_tpl->tpl_vars['itemdata2']->value['description'])));?>
</td></tr>
    <?php
$_smarty_tpl->tpl_vars['itemdata2'] = $foreach_itemdata2_Sav;
}
?>
</table>
<?php }
}
?>