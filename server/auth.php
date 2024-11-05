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
    // Пароль совпал, проверяем роль пользователя
    if ($permissions == 1) {
        // Подключение к базе данных через пользователя учителя
        $db = new mysqli('localhost', 'teacher_user', ']D)fD1NIiP[K/P5f', 'gradestudent');
    } elseif ($permissions == 0) {
        // Подключение к базе данных через пользователя студента
        $db = new mysqli('localhost', 'student_user', 'kEmBkAUzYqFpvHrd', 'gradestudent');
    } else {
        // Подключение к базе данных через пользователя секретаря
        $db = new mysqli('localhost', 'secretary_user', ']Ln8gu-JE9TwU4]2', 'gradestudent');
    }

    if ($db->connect_error) {
        die("Connection failed: " . $db->connect_error);
    }

    $data = [];

    // Отправка прав пользователя
    $data['permissions'] = $permissions;

    if ($permissions == 1) {
        // Запрос для учителя
        $query = "
            SELECT 
		g.grade_id,
                d.discipline_name, 
                t.full_name AS teacher_name, 
                s.full_name AS student_name, 
		g.teacher_id,
		g.student_id,
                g.exam_type, 
                g.grade_100, 
                g.grade_5, 
                g.grade_date,
		g.semester
            FROM Grades g
            JOIN Teacher t ON g.teacher_id = t.teacher_id
            JOIN Student s ON g.student_id = s.student_id
            JOIN Discipline d ON g.discipline_id = d.discipline_id
            WHERE g.teacher_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['grades'][] = $row;
        }
        $stmt->close();

        // Получение направлений учителя и групп учителя
        $query = "
            SELECT 
                d.direction_name, 
                sg.group_name
            FROM DirectionTeacher dt
            JOIN Direction d ON dt.direction_id = d.direction_id
            JOIN StudentGroup sg ON d.direction_id = sg.direction_id
            WHERE dt.teacher_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['directions_groups'][] = $row;
        }
        $stmt->close();

        // Получение списка участников групп
        $query = "
            SELECT 
		s.student_id,
                sg.group_name, 
                s.full_name AS student_name, 
                s.email, 
                s.phone
            FROM StudentGroupLink sgl
            JOIN StudentGroup sg ON sgl.group_id = sg.group_id
            JOIN Student s ON sgl.student_id = s.student_id
            WHERE sg.group_id IN (SELECT group_id FROM StudentGroup WHERE direction_id IN (SELECT direction_id FROM DirectionTeacher WHERE teacher_id = ?))
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['group_members'][] = $row;
        }
        $stmt->close();

        // Получение дисциплин учителя
        $query = "
            SELECT 
		d.discipline_id,
                d.discipline_name, 
                d.department_location
            FROM TeacherDiscipline td
            JOIN Discipline d ON td.discipline_id = d.discipline_id
            WHERE td.teacher_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['disciplines'][] = $row;
        }
        $stmt->close();

        // Получение ФИО, email и телефона учителя
        $query = "
            SELECT 
		teacher_id,
                full_name, 
                email, 
                phone
            FROM Teacher
            WHERE teacher_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['teacher_info'][] = $row;
        }
        $stmt->close();

        // Получение списка всех учителей
        $query = "
            SELECT 
                full_name, 
                email, 
                phone
            FROM Teacher
        ";
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['all_teachers'][] = $row;
        }
        $stmt->close();

        // Получение списка всех секретарей
        $query = "
            SELECT 
                full_name, 
                email, 
                phone
            FROM Secretary
        ";
        $stmt = $db->prepare($query);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['all_secretaries'][] = $row;
        }
        $stmt->close();

    } elseif ($permissions == 0) {
        // Запрос для студента
        $query = "
            SELECT 
                s.full_name AS student_name, 
                t.full_name AS teacher_name, 
                d.discipline_name, 
                g.exam_type, 
                g.grade_100, 
                g.grade_5, 
                g.grade_date,
		g.semester
            FROM Grades g
            JOIN Student s ON g.student_id = s.student_id
            JOIN Teacher t ON g.teacher_id = t.teacher_id
            JOIN Discipline d ON g.discipline_id = d.discipline_id
            WHERE g.student_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['grades'][] = $row;
        }
        $stmt->close();

        // Получение данных о группе студента
        $query = "
            SELECT 
                sg.group_name, 
                s.full_name AS student_name, 
                s.email, 
                s.phone,
                d.direction_name,
                d.faculty_name
            FROM StudentGroupLink sgl
            JOIN StudentGroup sg ON sgl.group_id = sg.group_id
            JOIN Student s ON sgl.student_id = s.student_id
            JOIN Direction d ON sg.direction_id = d.direction_id
            WHERE sgl.student_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['group'][] = $row;
        }
        $stmt->close();

        // Получение данных о всех одногруппниках
        $query = "
            SELECT 
                s.full_name, 
                s.email, 
                s.phone
            FROM StudentGroupLink sgl
            JOIN Student s ON sgl.student_id = s.student_id
            WHERE sgl.group_id = (SELECT group_id FROM StudentGroupLink WHERE student_id = ?)
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['groupmates'][] = $row;
        }
        $stmt->close();

        // Запрос для получения преподавателей и их контактов
        $query = "
            SELECT 
                t.full_name AS teacher_name, 
                t.phone, 
                t.email
            FROM Teacher t
            JOIN TeacherDiscipline td ON t.teacher_id = td.teacher_id
            JOIN Discipline d ON td.discipline_id = d.discipline_id
            JOIN DisciplineDirection dd ON d.discipline_id = dd.discipline_id
            JOIN StudentGroup sg ON dd.direction_id = sg.direction_id
            JOIN StudentGroupLink sgl ON sg.group_id = sgl.group_id
            WHERE sgl.student_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['teachers'][] = $row;
        }
        $stmt->close();

        // Запрос для получения дисциплин и расположения кафедры
        $query = "
            SELECT 
		d.discipline_name, 
                d.department_location
            FROM Discipline d
            JOIN DisciplineDirection dd ON d.discipline_id = dd.discipline_id
            JOIN StudentGroup sg ON dd.direction_id = sg.direction_id
            JOIN StudentGroupLink sgl ON sg.group_id = sgl.group_id
            WHERE sgl.student_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['disciplines'][] = $row;
        }
        $stmt->close();
    } elseif ($permissions == 2) {
        // Запрос для секретаря
        $query = "
            SELECT 
                full_name, 
                email, 
                phone
            FROM Secretary
            WHERE secretary_id = ?
        ";
        $stmt = $db->prepare($query);
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $data['secretary_info'][] = $row;
        }
        $stmt->close();

$query = "
    SELECT 
        user_id, 
        login, 
        full_name, 
        email, 
        phone, 
        permissions
    FROM User
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['users'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        direction_id, 
        direction_name, 
        faculty_name
    FROM Direction
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['directions'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        group_id, 
        group_name, 
        direction_id
    FROM StudentGroup
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['student_groups'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        student_id, 
        full_name, 
        email, 
        phone
    FROM Student
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['students'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        group_id, 
        student_id
    FROM StudentGroupLink
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['student_group_links'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        teacher_id, 
        full_name, 
        email, 
        phone
    FROM Teacher
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['all_teachers'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        discipline_id, 
        discipline_name, 
        department_location
    FROM Discipline
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['disciplines'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        direction_id, 
        teacher_id
    FROM DirectionTeacher
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['direction_teachers'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        teacher_id, 
        discipline_id
    FROM TeacherDiscipline
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['teacher_disciplines'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        secretary_id, 
        full_name, 
        email, 
        phone
    FROM Secretary
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['all_secretaries'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        discipline_id, 
        direction_id
    FROM DisciplineDirection
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['discipline_directions'][] = $row;
}
$stmt->close();

$query = "
    SELECT 
        temp_user_id, 
        login, 
        full_name, 
        email, 
        phone, 
        disciplines, 
        permissions, 
        created_at
    FROM TempUser
";
$stmt = $db->prepare($query);
$stmt->execute();
$result = $stmt->get_result();
while ($row = $result->fetch_assoc()) {
    $data['temp_users'][] = $row;
}
$stmt->close();

    }

    if (empty($data)) {
        die(json_encode(['status' => 'error', 'message' => 'No data found']));
    }

    // Отправка результатов в формате JSON
    header('Content-Type: application/json');
    echo json_encode(['status' => 'success', 'data' => $data]);
} else {
    // Отправка ошибки в формате JSON
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error', 'message' => 'Invalid password']);
}
?>