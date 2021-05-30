<?php /* Smarty version 3.1.24, created on 2017-09-08 20:12:05
         compiled from "/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/university.tpl" */ ?>
<?php
/*%%SmartyHeaderCode:96705036359b27b05d2be32_33542701%%*/
if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    '9b69473f53acdd5e04ce0cbce506f2167813dd0f' => 
    array (
      0 => '/home/valkyrie/online_strage/Dropbox/Public/Website/Spider/templates/university.tpl',
      1 => 1504233200,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '96705036359b27b05d2be32_33542701',
  'variables' => 
  array (
    'item1' => 0,
    'itemdata1' => 0,
  ),
  'has_nocache_code' => false,
  'version' => '3.1.24',
  'unifunc' => 'content_59b27b05d313b2_59671963',
),false);
/*/%%SmartyHeaderCode%%*/
if ($_valid && !is_callable('content_59b27b05d313b2_59671963')) {
function content_59b27b05d313b2_59671963 ($_smarty_tpl) {
if (!is_callable('smarty_modifier_auto_link')) require_once 'Spider/smarty_plugin/modifier.auto_link.php';

$_smarty_tpl->properties['nocache_hash'] = '96705036359b27b05d2be32_33542701';
?>
<h2>西日本の大学総合力ランキング 2018</h2>
<p class="ss1">
・高被引用論文数は２０１7年４月に公開されたクラリベイト・アナリティクスのデータ<br/>
・科学研究費配分額は平成２8年度のデータ<br/>
・医師国家試験は平成２７年度のデータ<br/>
・司法試験は平成28年度のデータ<br/>
・公認会計士試験は平成２７年度のデータ<br/>
・歯科医師国家試験は平成２７年度のデータ<br/>
・薬剤師国家試験は平成２７年度のデータ<br/>
・一級建築士国家試験は平成２8年度のデータ<br/>
・弁理士国家試験は平成２７年度のデータ<br/>
・獣医師国家試験は平成２７年度のデータ<br/>
・社会福祉士国家試験は2015年のデータ<br/>
・看護師国家試験は2015年のデータ<br/>
・警察官・消防士・自衛官・教員・キャビンアテンダントは２０１４年のデータ<br/>
・全国の出身大学別社長データは２０１５年１月に帝国データバンクが公開したもの<br/>
・主要325社就職者数は2015年度のもの<br/>
・科学研究費は平成27年度のデータ<br/>
・私立大学等経常費補助金は平成27年度のデータ<br/>
・国立大学運営費交付金は平成28年度のデータ
</p>
<p class="ss2">
西日本にある大学は、国立の一流大学から私立中堅大学まで幅広く揃っています。<br/>

予備校などでは旧来より大学郡を作って、長らく予備校のコースを宣伝するのに使ってきた呼び方やネットでの呼び方があります。<br/>

旧帝国大 - 国立の一流大学。西日本では、京都大学・大阪大学・名古屋大学・九州大学。<br/>

三商大 - 社会科学で定評のある国公立の実力校。西日本では、神戸大・大阪市立大。<br/>

金岡千広 - 国立総合大学の実力校。西日本では、金沢大・岡山大・広島大。<br/>

農繊名電 - 国立理工系の実力校。西日本では、名古屋工業大学・京都工芸繊維大学。<br/>

関関同立 - 関西の有名大手私立総合大学。同志社大学・関西学院大学・立命館大学・関西大学。<br/>

産近甲龍 - 関西の有名中堅私立総合大学。京都産業大学・近畿大学・甲南大学・龍谷大学。<br/>

外外経工佛 - 関西の老舗私立単科大学。関西外国語大学・京都外国語大学・大阪経済大学・大阪工業大学・佛教大学。<br/>

この他にも、国立医科大や女子大や教育大や薬科大など多彩なジャンルの大学が揃っています。<br/>
</p>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">大学名</th><th class="des">説明</th></tr>
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