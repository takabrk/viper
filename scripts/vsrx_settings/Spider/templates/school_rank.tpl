<h2>関西の高校総合力ランキング 2018</h2>
<p class="ss1">
2017年にサンデー毎日で集計された数字を基にしています。<br/>
東京大・京都大・大阪大の合格者数でランキング化しています。
</p>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">高校名</th><th class="des">説明</th></tr>
    {foreach $item1 as $itemdata1}
        <tr class="tre"><td class="uni1">{$itemdata1.id}</td><td class="uni2">{$itemdata1.name}</td><td class="des">{$itemdata1.description|nl2br|strip:" "|auto_link}</td></tr>
    {/foreach}
</table>
