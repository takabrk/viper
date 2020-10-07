<?php
function smarty_modifier_auto_link($string, $type = 'url'){

    $regstr = "/((?:https?|ftp):\/\/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+$,%#]+)/u";
    switch ($type) {
        case 'url':
            return preg_replace($regstr,'<a href="\\0" target="_blank" title="\\0">\\0</a>', $string);
            break;
        default:
            return $string;
    }
}
?>