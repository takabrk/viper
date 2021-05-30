<?php /* Smarty version 3.1.24, created on 2017-09-08 20:12:05
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school_rank.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:132156901259b27b05d504c7_86863571%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '0dc008b5f5aac4e00580fef0b98bbf4327b3e9dd' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school_rank.tpl',
      1 => 1504233209,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '132156901259b27b05d504c7_86863571',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b27b05d55c09_96561955',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b27b05d55c09_96561955')) {
function content_59b27b05d55c09_96561955 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '132156901259b27b05d504c7_86863571';
?>
<h2>関西の高校総合力ランキング 2018</h2>
<p class="ss1">
2017年にサンデー毎日で集計された数字を基にしています。<br/>
東京大・京都大・大阪大の合格者数でランキング化しています。
</p>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">高校名</th><th class="des">説明</th></tr>
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