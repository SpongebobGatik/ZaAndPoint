<?php

require_once 'system/functions.php'; // стартуем функции

// Подключение к базе данных с пользователем, который имеет доступ только к таблице User
$db = new mysqli('localhost', 'view_user', '-)H)3bCfcF_VN69T', 'gradestudent');

if ($db->connect_error) {
    die("Connection failed: " . $db->connect_error);
}

// Получение данных из JSON-запроса
$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    die(json_encode(['status' => 'error', 'message' => 'Invalid JSON data']));
}

$login = protect($db, $data['username']);
$password = protect($db, $data['password']);

// Проверка наличия логина и соответствия пароля
$query = "SELECT user_id, password_hash, permissions FROM User WHERE login = ?";
$stmt = $db->prepare($query);
$stmt->bind_param("s", $login);
$stmt->execute();
$stmt->bind_result($user_id, $stored_password_hash, $permissions);
$stmt->fetch();
$stmt->close();

if (!$user_id) {
    die(json_encode(['status' => 'error', 'message' => 'User not found']));
}

// Проверка пароля
if (password_verify($password, $stored_password_hash)) {
    // Обновление данных пользователя
    $email = protect($db, $data['email']);
    $phone = protect($db, $data['phone']);
    
    $update_query = "UPDATE User SET email = ?, phone = ? WHERE user_id = ?";
    $update_stmt = $db->prepare($update_query);
    $update_stmt->bind_param("ssi", $email, $phone, $user_id);
    
    if ($update_stmt->execute()) {
        echo json_encode(['status' => 'success', 'message' => 'User information updated successfully']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Failed to update user information']);
    }
    
    $update_stmt->close();
} else {
    echo json_encode(['status' => 'error', 'message' => 'Incorrect password']);
}

$db->close();
?>
