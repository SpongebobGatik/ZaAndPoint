<?php

header('Content-Type: text/html; charset=UTF-8');

require_once 'system/functions.php'; // стартуем функции

// Подключение к базе данных с пользователем, который имеет доступ только к таблице User
$db = new mysqli('localhost', 'view_user', '-)H)3bCfcF_VN69T', 'gradestudent');
$db->set_charset('utf8');

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
    // Пароль совпал, проверяем роль пользователя
    if ($permissions == 1) {
        // Подключение к базе данных через пользователя учителя
        $db = new mysqli('localhost', 'teacher_user', ']D)fD1NIiP[K/P5f', 'gradestudent');
	$db->set_charset('utf8');
    }

    if ($permissions == 2) {
        // Подключение к базе данных через пользователя секретаря
        $db = new mysqli('localhost', 'secretary_user', ']Ln8gu-JE9TwU4]2', 'gradestudent');
	$db->set_charset('utf8');
    }

    if ($db->connect_error) {
        die("Connection failed: " . $db->connect_error);
    }

    // Обработка команды
    if ($data['command'] === 'insert_at') {
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$semester = protect($db, $data['data']['semester']);
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$student_id = protect($db, $data['data']['student_id']);
	$exam_type = protect($db, $data['data']['exam_type']);
	$grade_100 = protect($db, $data['data']['grade_100']);

        $query = "INSERT INTO Grades (grade_id, semester, student_id, teacher_id, discipline_id, exam_type, grade_100, grade_5, grade_date) VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL, NULL)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("iiisss", $semester, $student_id, $teacher_id, $discipline_id, $exam_type, $grade_100);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }elseif ($data['command'] === 'update_at') {
        $grade_id = protect($db, $data['data']['grade_id']);
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$semester = protect($db, $data['data']['semester']);
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$student_id = protect($db, $data['data']['student_id']);
	$exam_type = protect($db, $data['data']['exam_type']);
	$grade_100 = protect($db, $data['data']['grade_100']);

	$query = "UPDATE Grades SET discipline_id = ?, teacher_id = ?, student_id = ?, exam_type = ?, grade_100 = ?, grade_date = NULL WHERE grade_id = ?";
	$stmt = $db->prepare($query);
	$stmt->bind_param("iiisii", $discipline_id, $teacher_id, $student_id, $exam_type, $grade_100, $grade_id);
	$stmt->execute();
	$stmt->close();


        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);
    } elseif ($data['command'] === 'delete_at') {
        $grade_id = $data['data']['grade_id'];

        $query = "DELETE FROM Grades WHERE grade_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $grade_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data deleted successfully']);
    } elseif ($data['command'] === 'insert_temp') {
        $temp_user_id = protect($db, $data['data']['temp_user_id']);

// Подготовка запроса для получения данных из TempUser
$query = "SELECT login, password_hash, full_name, email, phone, permissions FROM TempUser WHERE temp_user_id = ?";
$stmt = $db->prepare($query);
$stmt->bind_param("i", $temp_user_id);
$stmt->execute();
$result = $stmt->get_result();
$temp_user = $result->fetch_assoc();
$stmt->close();

if ($temp_user) {
    // Подготовка запроса для вставки данных в таблицу User
    $query = "INSERT INTO User (login, password_hash, full_name, email, phone, permissions) VALUES (?, ?, ?, ?, ?, ?)";
    $stmt = $db->prepare($query);
    $stmt->bind_param("sssssi", $temp_user['login'], $temp_user['password_hash'], $temp_user['full_name'], $temp_user['email'], $temp_user['phone'], $temp_user['permissions']);
    $stmt->execute();
    $stmt->close();
    
    // Удаление пользователя из TempUser
    $query = "DELETE FROM TempUser WHERE temp_user_id = ?";
    $stmt = $db->prepare($query);
    $stmt->bind_param("i", $temp_user_id);
    $stmt->execute();
    $stmt->close();

    echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);
    }
}elseif ($data['command'] === 'update_temp') {
        $temp_user_id = protect($db, $data['data']['temp_user_id']);
	$username = protect($db, $data['data']['login']);
	$full_name = protect($db, $data['data']['full_name']);
	$email = protect($db, $data['data']['email']);
	$phone = protect($db, $data['data']['phone']);
	$disciplines = protect($db, $data['data']['disciplines']);
	$permissions = protect($db, $data['data']['permissions']);

	$query = "UPDATE TempUser SET login = ?, full_name = ?, email = ?, phone = ?, disciplines = ?, permissions = ? WHERE temp_user_id = ?";
	$stmt = $db->prepare($query);
	$stmt->bind_param("sssssii", $username, $full_name, $email, $phone, $disciplines, $permissions, $temp_user_id);
	$stmt->execute();
	$stmt->close();


        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);
    }elseif ($data['command'] === 'delete_temp') {
    $temp_user_id = protect($db, $data['data']['temp_user_id']);
    // Удаление пользователя из TempUser
    $query = "DELETE FROM TempUser WHERE temp_user_id = ?";
    $stmt = $db->prepare($query);
    $stmt->bind_param("i", $temp_user_id);
    $stmt->execute();
    $stmt->close();

    echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);
    }
    elseif ($data['command'] === 'insert_dir') {
	$direction_name = protect($db, $data['data']['direction_name']);
	$faculty_name = protect($db, $data['data']['faculty_name']);

        $query = "INSERT INTO direction (direction_id, direction_name, faculty_name) VALUES (NULL, ?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ss", $direction_name, $faculty_name);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_dirt') {
	$direction_id = protect($db, $data['data']['direction_id']);
	$teacher_id = protect($db, $data['data']['teacher_id']);

        $query = "INSERT INTO directionteacher (direction_id, teacher_id) VALUES (?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $direction_id, $teacher_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_dis') {
	$discipline_name = protect($db, $data['data']['discipline_name']);
	$department_location = protect($db, $data['data']['department_location']);

        $query = "INSERT INTO discipline (discipline_id, discipline_name, department_location) VALUES (NULL, ?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ss", $discipline_name, $department_location);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_disdir') {
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$direction_id = protect($db, $data['data']['direction_id']);

        $query = "INSERT INTO disciplinedirection (discipline_id, direction_id) VALUES (?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $discipline_id, $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_student') {
	$full_name = protect($db, $data['data']['full_name']);
	$email = protect($db, $data['data']['email']);
	$phone = protect($db, $data['data']['phone']);

        $query = "INSERT INTO student (student_id, full_name, email, phone) VALUES (NULL, ?, ?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("sss", $full_name, $email, $phone);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_st') {
	$group_name = protect($db, $data['data']['group_name']);
	$direction_id = protect($db, $data['data']['direction_id']);

        $query = "INSERT INTO studentgroup (group_id, group_name, direction_id) VALUES (NULL, ?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("si", $group_name, $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_gr') {
	$group_id = protect($db, $data['data']['group_id']);
	$student_id = protect($db, $data['data']['student_id']);

        $query = "INSERT INTO studentgrouplink (group_id, student_id) VALUES (?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $group_id, $student_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_tdis') {
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$discipline_id = protect($db, $data['data']['discipline_id']);

        $query = "INSERT INTO teacherdiscipline (teacher_id, discipline_id) VALUES (?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $teacher_id, $discipline_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
    elseif ($data['command'] === 'insert_user') {
	$full_name = protect($db, $data['data']['full_name']);
    $password = protect($db, $data['data']['password_hash']);
	$login = protect($db, $data['data']['login']);
	$email = protect($db, $data['data']['email']);
	$phone = protect($db, $data['data']['phone']);
	$permissions = protect($db, $data['data']['permissions']);
    $password_hash = password_hash($password, PASSWORD_BCRYPT);

        $query = "INSERT INTO User (user_id, login, password_hash, full_name, email, phone, permissions) VALUES (NULL, ?, ?, ?, ?, ?, ?)";
        $stmt = $db->prepare($query);
        $stmt->bind_param("sssssi", $login, $password_hash, $full_name, $email, $phone, $permissions);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data inserted successfully']);


 }
 elseif ($data['command'] === 'update_dir') {
    $direction_id = protect($db, $data['data']['direction_id']);
	$direction_name = protect($db, $data['data']['direction_name']);
	$faculty_name = protect($db, $data['data']['faculty_name']);

    $query = "UPDATE direction SET direction_name = ?, faculty_name = ? WHERE direction_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ssi", $direction_name, $faculty_name, $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_dirt') {
	$direction_id = protect($db, $data['data']['direction_id']);
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$direction_id_new = protect($db, $data['data']['direction_id_new']);
	$teacher_id_new = protect($db, $data['data']['teacher_id_new']);

    $query = "UPDATE directionteacher SET direction_id = ?, teacher_id = ? WHERE direction_id = ? AND teacher_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("iiii", $direction_id_new, $teacher_id_new, $direction_id, $teacher_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_dis') {
    $discipline_id = protect($db, $data['data']['discipline_id']);
	$discipline_name = protect($db, $data['data']['discipline_name']);
	$department_location = protect($db, $data['data']['department_location']);

    $query = "UPDATE discipline SET discipline_name = ?, department_location = ? WHERE discipline_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ssi", $discipline_name, $department_location, $discipline_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_disdir') {
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$direction_id = protect($db, $data['data']['direction_id']);
	$discipline_id_new = protect($db, $data['data']['discipline_id_new']);
	$direction_id_new = protect($db, $data['data']['direction_id_new']);

    $query = "UPDATE disciplinedirection SET discipline_id = ?, direction_id = ? WHERE discipline_id = ? AND direction_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("iiii", $discipline_id_new, $direction_id_new, $discipline_id, $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_student') {
    $student_id = protect($db, $data['data']['student_id']);
	$full_name = protect($db, $data['data']['full_name']);
	$email = protect($db, $data['data']['email']);
	$phone = protect($db, $data['data']['phone']);

    $query = "UPDATE student SET full_name = ?, email = ?, phone = ? WHERE student_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("sssi", $full_name, $email, $phone, $student_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_st') {
    $group_id = protect($db, $data['data']['group_id']);
	$group_name = protect($db, $data['data']['group_name']);
	$direction_id = protect($db, $data['data']['direction_id']);

    $query = "UPDATE studentgroup SET group_name = ?, direction_id = ? WHERE group_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("sii", $group_name, $direction_id, $group_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_gr') {
	$group_id = protect($db, $data['data']['group_id']);
	$student_id = protect($db, $data['data']['student_id']);
	$group_id_new = protect($db, $data['data']['group_id_new']);
	$student_id_new = protect($db, $data['data']['student_id_new']);

    $query = "UPDATE studentgrouplink SET group_id = ?, student_id = ? WHERE group_id = ? AND student_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("iiii", $group_id_new, $student_id_new, $group_id, $student_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'update_tdis') {
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$teacher_id_new = protect($db, $data['data']['teacher_id_new']);
	$discipline_id_new = protect($db, $data['data']['discipline_id_new']);

    $query = "UPDATE teacherdiscipline SET teacher_id = ?, discipline_id = ? WHERE teacher_id = ? AND discipline_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("iiii", $teacher_id_new, $discipline_id_new, $teacher_id, $discipline_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
elseif ($data['command'] === 'update_user') {
    $user_id = protect($db, $data['data']['user_id']);
    $full_name = protect($db, $data['data']['full_name']);
    $login = protect($db, $data['data']['login']);
    $email = protect($db, $data['data']['email']);
    $phone = protect($db, $data['data']['phone']);
    $permissions = protect($db, $data['data']['permissions']);

    $query = "UPDATE user SET login = ?, full_name = ?, email = ?, phone = ?, permissions = ?";
    $params = [$login, $full_name, $email, $phone, $permissions];

    // Проверяем, передан ли новый пароль
    if (!empty($data['data']['password_hash'])) {
        $password_hash = password_hash(protect($db, $data['data']['password_hash']), PASSWORD_BCRYPT);
        $query .= ", password_hash = ?";
        $params[] = $password_hash;
    }

    $query .= " WHERE user_id = ?";
    $params[] = $user_id; 

    $stmt = $db->prepare($query);

    // Динамически формируем строку типов параметров
    $types = str_repeat("s", count($params) - 1) . "i"; 
    $stmt->bind_param($types, ...$params); 

    $stmt->execute();
    $stmt->close();

    echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);
}
 elseif ($data['command'] === 'delete_dir') {
    $direction_id = protect($db, $data['data']['direction_id']);

    $query = "DELETE FROM direction WHERE direction_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_dirt') {
	$direction_id = protect($db, $data['data']['direction_id']);
	$teacher_id = protect($db, $data['data']['teacher_id']);

    $query = "DELETE FROM directionteacher WHERE direction_id = ? AND teacher_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $direction_id, $teacher_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_dis') {
    $discipline_id = protect($db, $data['data']['discipline_id']);

    $query = "DELETE FROM discipline WHERE discipline_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $discipline_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_disdir') {
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$direction_id = protect($db, $data['data']['direction_id']);

    $query = "DELETE FROM disciplinedirection WHERE discipline_id = ? AND direction_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $discipline_id, $direction_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_student') {
    $student_id = protect($db, $data['data']['student_id']);

    $query = "DELETE FROM student WHERE student_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $student_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_st') {
    $group_id = protect($db, $data['data']['group_id']);

    $query = "DELETE FROM studentgroup WHERE group_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $group_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_gr') {
	$group_id = protect($db, $data['data']['group_id']);
	$student_id = protect($db, $data['data']['student_id']);

    $query = "DELETE FROM studentgrouplink WHERE group_id = ? AND student_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $group_id, $student_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_tdis') {
	$teacher_id = protect($db, $data['data']['teacher_id']);
	$discipline_id = protect($db, $data['data']['discipline_id']);
	$teacher_id_new = protect($db, $data['data']['teacher_id_new']);
	$discipline_id_new = protect($db, $data['data']['discipline_id_new']);

    $query = "DELETE FROM teacherdiscipline WHERE teacher_id = ? AND discipline_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("ii", $teacher_id, $discipline_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
    elseif ($data['command'] === 'delete_user') {
    $user_id = protect($db, $data['data']['user_id']);

    $query = "DELETE FROM user WHERE user_id = ?";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $stmt->close();

        echo json_encode(['status' => 'success', 'message' => 'Data updated successfully']);


 }
else {
        echo json_encode(['status' => 'error', 'message' => 'Invalid command']);
    }
} else {
    die(json_encode(['status' => 'error', 'message' => 'Invalid password']));
}

?>
