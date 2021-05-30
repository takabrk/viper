<?php /* Smarty version 3.1.24, created on 2017-10-06 04:31:41
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/news.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:86704707059d6889d2ee756_27317261%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'fbe79a641587aaa401d1ae583b1d42b48393e90b' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/news.tpl',
      1 => 1507228715,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '86704707059d6889d2ee756_27317261',
  'variables' => 
  array (
    'item2' => 0,
    'itemdata2' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59d6889d2f2479_75426689',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59d6889d2f2479_75426689')) {
function content_59d6889d2f2479_75426689 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '86704707059d6889d2ee756_27317261';
?>
<table class="anp">
    <tr class="tre"><th class="uni2">名称</th><th class="des">URL</th></tr>
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
        <tr class="tre" id="<?php echo $_smarty_tpl->tpl_vars['itemdata2']->value['id'];?>
"><td class="uni2"><?php echo $_smarty_tpl->tpl_vars['itemdata2']->value['name'];?>
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