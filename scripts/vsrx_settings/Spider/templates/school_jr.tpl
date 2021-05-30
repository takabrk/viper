<h2>大阪の中学校ランキング 2017</h2>
<p class="ss1">
国立3校、私立上位校、北摂や天王寺などにある一部の公立中学校は、教育レベルが高く、高校進学時に難関校に数多く合格、あるいは内部進学します。<br/>
私立の下位校やほとんどの公立中学校へ進学した場合、将来的に就職や進学でかなり苦労する事になりますので、中学レベルでもよく考えて学校選びをした方が良いでしょう。
</p>
<table class="university">
    <tr class="tre"><th class="uni1">順位</th><th class="uni2">中学校名</th><th class="des">説明</th></tr>
    {foreach $item1 as $itemdata1}
        <tr class="tre"><td class="uni1">{$itemdata1.id}</td><td class="uni2">{$itemdata1.name}</td><td class="des">{$itemdata1.description|nl2br|strip:" "|auto_link}</td></tr>
    {/foreach}
</table>
