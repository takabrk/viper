<h2>大阪の地域別総合力ランキング 2018</h2>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">地域名</th><th class="des">説明</th></tr>
    {foreach $item1 as $itemdata1}
        <tr class="tre"><td class="uni1">{$itemdata1.id}</td><td class="uni2">{$itemdata1.name}</td><td class="des">{$itemdata1.description|nl2br|strip:" "|auto_link}</td></tr>
    {/foreach}
</table>
