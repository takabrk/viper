<?php /* Smarty version 3.1.24, created on 2017-09-08 20:12:05
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school_jr.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:155165676559b27b05d60012_16708019%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '78b56df262c765a0d2950179cd1682e768f6f4dc' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/school_jr.tpl',
      1 => 1504233952,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '155165676559b27b05d60012_16708019',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b27b05d65934_58528915',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b27b05d65934_58528915')) {
function content_59b27b05d65934_58528915 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '155165676559b27b05d60012_16708019';
?>
<h2>大阪の中学校ランキング 2017</h2>
<p class="ss1">
国立3校、私立上位校、北摂や天王寺などにある一部の公立中学校は、教育レベルが高く、高校進学時に難関校に数多く合格、あるいは内部進学します。<br/>
私立の下位校やほとんどの公立中学校へ進学した場合、将来的に就職や進学でかなり苦労する事になりますので、中学レベルでもよく考えて学校選びをした方が良いでしょう。
</p>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">中学校名</th><th class="des">説明</th></tr>
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