<?php
header("Content-Type: text/html; charset=utf-8");
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="jv/jsonview-core.css" />
        <link rel="stylesheet" type="text/css" href="jv/jsonview.css" />
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" type="text/javascript"></script>
        <script src="jv/background.js" type="text/javascript"></script>
        <script src="jv/content.js" type="text/javascript"></script>
        <script src="jv/workerFormatter.js" type="text/javascript"></script>
        <script src="jv/workerJSONLint.js" type="text/javascript"></script>
        <title>GDQ JSON</title>
    </head>
    <body>
        <p><code></code></p>
        <div class="toolbox">
            <a href="//b303.me/gdq/schedule.json">View source</a><br />
            <a href="http://validator.w3.org/check?uri=https://b303.me/gdq/">
            <img src="valid-xhtml10.png" alt="Valid XHTML 1.0 Strict" width="109" />
            </a><br />
            <a href="http://jsonview.com">With thanks to <img src="jv/jsonview16.png" alt="JSONView logo 16px" /></a><br />
            <b>Contents:</b>
            <ul>
                <li><a href="#info">Info</a></li>
                <li><a href="#schedule">Schedule</a></li>
                <li><a href="#current">Current</a></li>
            </ul>
        </div>
        <script type="text/javascript">
            $.getJSON('./<?php if (isset($_GET['data']) && file_exists($_GET['data'] . ".json")) { echo $_GET['data']; } else { echo "schedule"; } ?>.json', function(json) {
              $('code').html(jsonToHTML(json, null));
            });
        </script>
    </body>
</html>
