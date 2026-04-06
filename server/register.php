<?php

require_once 'system/functions.php';

$requestLogFile = 'request_log.json';

$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    die(json_encode(['status' => 'error', 'message' => 'Invalid JSON data']));
}

$ip = $_SERVER['REMOTE_ADDR'];
$currentTime = time();

$requestLogs = [];
if (file_exists($requestLogFile)) {
    $requestLogs = json_decode(file_get_contents($requestLogFile), true);
    if (!is_array($requestLogs)) {
        $requestLogs = [];
    }
}

$requestLogs = array_filter($requestLogs, function($log) use ($currentTime) {
    return ($currentTime - $log['time']) < 3600;
});

$requestCount = 0;
foreach ($requestLogs as $log) {
    if ($log['ip'] === $ip) {
        $requestCount++;
    }
}

if ($requestCount >= 10) {
    die(json_encode(['status' => 'error code 401', 'message' => 'Request limit exceeded']));
}

$requestLogs[] = ['ip' => $ip, 'time' => $currentTime];

file_put_contents($requestLogFile, json_encode($requestLogs));

$command = $data['command'] ?? '';

if ($command === 'register') {
    $db = new mysqli('localhost', 'view_user', '-)H)3bCfcF_VN69T', 'gradestudent');

    if ($db->connect_error) {
        die("Connection failed: " . $db->connect_error);
    }

    $login = protect($db, $data['login']);
    $password = protect($db, $data['password']);
    $full_name = protect($db, $data['full_name']);
    $email = protect($db, $data['email']);
    $phone = protect($db, $data['phone']);
    $disciplines = protect($db, $data['disciplines']);
    $permissions = protect($db, $data['permissions']);

    if (!preg_match('/^[A-Za-z0-9]+$/', $login)) {
        die(json_encode(['status' => 'error code 402', 'message' => 'Login must contain only English characters']));
    }

    if (!preg_match('/^[А-Яа-яЁё\s]+$/u', $full_name)) {
        die(json_encode(['status' => 'error code 403', 'message' => 'Full name must contain only Russian characters']));
    }

    $password_hash = password_hash($password, PASSWORD_BCRYPT);

    if ($disciplines === '') {
        $stmt = $db->prepare("INSERT INTO TempUser (login, password_hash, full_name, email, phone, permissions) VALUES (?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("sssssi", $login, $password_hash, $full_name, $email, $phone, $permissions);
    } else {
        $stmt = $db->prepare("INSERT INTO TempUser (login, password_hash, full_name, email, phone, disciplines, permissions) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("ssssssi", $login, $password_hash, $full_name, $email, $phone, $disciplines, $permissions);
    }

    if ($stmt->execute()) {
        echo json_encode(['status' => 'success', 'message' => 'User registered successfully']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Failed to register user']);
    }

    $stmt->close();
    $db->close();
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid command']);
}
?>
