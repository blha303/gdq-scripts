<?php
header("Access-Control-Allow-Origin: *");
$info = json_decode(file_get_contents(realpath(dirname(__FILE__)) . "/schedule.json"), true);
print $info["current"]["until"];
