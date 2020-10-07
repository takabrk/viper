<table class="anp">
    <tr class="tre"><th class="uni2">名称</th><th class="des">URL</th></tr>
    {foreach $item2 as $itemdata2}
        <tr class="tre" id="{$itemdata2.id}"><td class="uni2">{$itemdata2.name}</td><td class="des">{$itemdata2.description|nl2br|strip:" "|auto_link}</td></tr>
    {/foreach}
</table>
