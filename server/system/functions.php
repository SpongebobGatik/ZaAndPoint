<?php
global $db;

/* Функция защиты от нежелательных действий */
function protect($db, $text) {
    return trim(mysqli_real_escape_string($db, htmlspecialchars($text, ENT_QUOTES, 'utf-8')));
}
?>
