<?php
header("Access-Control-Allow-Origin: *");
$songinfo = json_decode(file_get_contents(realpath(dirname(__FILE__)) . "/schedule.json"), true);
foreach ($songinfo["schedule"] as $d) {
  if ($d["ts"] > (time()-1200)) {
    break;
  }
}
if (isset($_GET['bbcode'])) {
  $fmt = "Now playing: [b]%s[b], being run by [b]%s[b]. Estimated time: [b]%s[b]";
} else {
  $fmt = "Now playing: %s, being run by %s. Estimated time: %s";
}
if (isset($_GET['alert'])) {
  header('Content-Type: text/javascript');
  print "alert(\"";
}
print sprintf($fmt, $d["game"], implode(", ", $d["runners"]), $d["runTime"]);
if (isset($_GET['alert'])) {
  print "\")";
}
