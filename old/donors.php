<?php
header("Content-Type: text/html; charset=utf-8");
?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="jsonview-core.css" />
        <link rel="stylesheet" type="text/css" href="jsonview.css" />
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" type="text/javascript"></script>
        <script src="background.js" type="text/javascript"></script>
        <script src="content.js" type="text/javascript"></script>
        <script src="workerFormatter.js" type="text/javascript"></script>
        <script src="workerJSONLint.js" type="text/javascript"></script>
        <title>AGDQ Donors JSON</title>
    </head>
    <body>
        <p><code></code></p>
        <div class="toolbox">
            <a href="http://blha303.com.au/agdq/donors.json">View source</a><br />
            <a href="http://validator.w3.org/check?uri=referer">
            <img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" width="109" />
            </a><br />
            <a href="http://jsonview.com">With thanks to <img src="jsonview16.png" alt="JSONView logo 16px" /></a><br />
            <b>Contents:</b>
            <ul>
                <li><a href="#info">Info</a></li>
                <li><a href="#donors">Donors</a></li>
            </ul>
        </div>
        <script type="text/javascript">
            $.getJSON('./donors.json', function(json) {
              $('code').html(jsonToHTML(json, null));
            });
        </script>
    </body>
</html>
