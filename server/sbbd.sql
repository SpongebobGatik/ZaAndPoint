CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(191) UNIQUE,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    permissions TINYINT
);

CREATE TABLE Direction (
    direction_id INT PRIMARY KEY AUTO_INCREMENT,
    direction_name VARCHAR(255),
    faculty_name VARCHAR(255)
);

CREATE TABLE StudentGroup (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255),
    direction_id INT,
    FOREIGN KEY (direction_id) REFERENCES Direction(direction_id)
);

CREATE TABLE Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE StudentGroupLink (
    group_id INT,
    student_id INT,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES StudentGroup(group_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

CREATE TABLE Teacher (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE Discipline (
    discipline_id INT PRIMARY KEY AUTO_INCREMENT,
    discipline_name VARCHAR(255),
    department_location VARCHAR(255)
);

CREATE TABLE DirectionTeacher (
    direction_id INT,
    teacher_id INT,
    PRIMARY KEY (direction_id, teacher_id),
    FOREIGN KEY (direction_id) REFERENCES Direction(direction_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

CREATE TABLE TeacherDiscipline (
    teacher_id INT,
    discipline_id INT,
    PRIMARY KEY (teacher_id, discipline_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id),
    FOREIGN KEY (discipline_id) REFERENCES Discipline(discipline_id)
);

CREATE TABLE Secretary (
    secretary_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE Grades (
    grade_id INT PRIMARY KEY AUTO_INCREMENT,
    semester INT CHECK (semester BETWEEN 1 AND 11),
    student_id INT,
    teacher_id INT,
    discipline_id INT,
    exam_type ENUM('зачёт', 'экзамен'),
    grade_100 INT,
    grade_5 VARCHAR(20),
    grade_date DATE,
    FOREIGN KEY (teacher_id, discipline_id) REFERENCES TeacherDiscipline(teacher_id, discipline_id)
);

CREATE TABLE DisciplineDirection (
    discipline_id INT,
    direction_id INT,
    PRIMARY KEY (discipline_id, direction_id),
    FOREIGN KEY (discipline_id) REFERENCES Discipline(discipline_id),
    FOREIGN KEY (direction_id) REFERENCES Direction(direction_id)
);

CREATE TABLE TempUser (
    temp_user_id INT PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(191) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    disciplines TEXT,
    permissions TINYINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER before_insert_user
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    IF NEW.login NOT REGEXP '^[A-Za-z0-9]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login must contain only English character and numberss';
    END IF;
    IF NEW.full_name NOT REGEXP '^[А-Яа-яЁё\\s]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Full name must contain only Russian characters';
    END IF;
END//

CREATE TRIGGER before_update_user
BEFORE UPDATE ON User
FOR EACH ROW
BEGIN
    IF NEW.login NOT REGEXP '^[A-Za-z0-9]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login must contain only English characters and numbers';
    END IF;
    IF NEW.full_name NOT REGEXP '^[А-Яа-яЁё\\s]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Full name must contain only Russian characters';
    END IF;
END//

CREATE TRIGGER after_insert_user
AFTER INSERT ON User
FOR EACH ROW
BEGIN
    IF NEW.permissions = 1 THEN
        INSERT INTO Teacher (teacher_id, full_name, email, phone)
        VALUES (NEW.user_id, NEW.full_name, NEW.email, NEW.phone);
    ELSEIF NEW.permissions = 0 THEN
        INSERT INTO Student (student_id, full_name, email, phone)
        VALUES (NEW.user_id, NEW.full_name, NEW.email, NEW.phone);
        
        -- Получить group_id группы "Нераспределённые студенты"
        SET @unassigned_group_id = (SELECT group_id FROM StudentGroup WHERE group_name = 'Нераспределённые студенты');
        -- Добавить студента в группу "Нераспределённые студенты"
        INSERT INTO StudentGroupLink (group_id, student_id) VALUES (@unassigned_group_id, NEW.user_id);
    ELSEIF NEW.permissions = 2 THEN
        INSERT INTO Secretary (secretary_id, full_name, email, phone)
        VALUES (NEW.user_id, NEW.full_name, NEW.email, NEW.phone);
    END IF;
END//

CREATE TRIGGER after_update_user
AFTER UPDATE ON User
FOR EACH ROW
BEGIN
    IF NEW.permissions = 1 THEN
        UPDATE Teacher
        SET full_name = NEW.full_name, email = NEW.email, phone = NEW.phone
        WHERE teacher_id = NEW.user_id;
    ELSEIF NEW.permissions = 0 THEN
        UPDATE Student
        SET full_name = NEW.full_name, email = NEW.email, phone = NEW.phone
        WHERE student_id = NEW.user_id;
    ELSEIF NEW.permissions = 2 THEN
        UPDATE Secretary
        SET full_name = NEW.full_name, email = NEW.email, phone = NEW.phone
        WHERE secretary_id = NEW.user_id;
    END IF;
END//
DELIMITER ;

DELIMITER //

CREATE TRIGGER before_insert_tempuser
BEFORE INSERT ON TempUser 
FOR EACH ROW
BEGIN
    -- Проверка на правильность логина
    IF NEW.login NOT REGEXP '^[A-Za-z0-9]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login must contain only English characters and numbers';
    END IF;

    -- Проверка на правильность полного имени
    IF NEW.full_name NOT REGEXP '^[А-Яа-яЁё \\s]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Full name must contain only Russian characters';
    END IF;

    -- Проверка на уникальность логина
    IF EXISTS (SELECT 1 FROM User WHERE login = NEW.login) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login already exists in the User table';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_update_tempuser
BEFORE UPDATE ON TempUser  
FOR EACH ROW
BEGIN
    -- Проверка на правильность логина
    IF NEW.login NOT REGEXP '^[A-Za-z0-9]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login must contain only English characters and numbers';
    END IF;

    -- Проверка на правильность полного имени
    IF NEW.full_name NOT REGEXP '^[А-Яа-яЁё \\s]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Full name must contain only Russian characters';
    END IF;

    -- Проверка на уникальность логина
    IF EXISTS (SELECT 1 FROM TempUser  WHERE login = NEW.login AND temp_user_id != NEW.temp_user_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login already exists in the TempUser  table';
    END IF;

    -- Проверка на уникальность логина в основной таблице User
    IF EXISTS (SELECT 1 FROM User WHERE login = NEW.login) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Login already exists in the User table';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_insert_grades
BEFORE INSERT ON Grades
FOR EACH ROW
BEGIN
    IF NEW.exam_type = 'зачёт' THEN
        IF NEW.grade_100 >= 50 THEN
            SET NEW.grade_5 = 'зачтено';
        ELSE
            SET NEW.grade_5 = 'незачтено';
        END IF;
    ELSEIF NEW.exam_type = 'экзамен' THEN
        IF NEW.grade_100 BETWEEN 87 AND 100 THEN
            SET NEW.grade_5 = 'отлично';
        ELSEIF NEW.grade_100 BETWEEN 73 AND 86 THEN
            SET NEW.grade_5 = 'хорошо';
        ELSEIF NEW.grade_100 BETWEEN 50 AND 72 THEN
            SET NEW.grade_5 = 'удовлетворительно';
        ELSE
            SET NEW.grade_5 = 'неудовлетворительно';
        END IF;
    END IF;
    SET NEW.grade_date = CURDATE();
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_update_grades
BEFORE UPDATE ON Grades
FOR EACH ROW
BEGIN
    IF NEW.exam_type = 'зачёт' THEN
        IF NEW.grade_100 >= 50 THEN
            SET NEW.grade_5 = 'зачтено';
        ELSE
            SET NEW.grade_5 = 'незачтено';
        END IF;
    ELSEIF NEW.exam_type = 'экзамен' THEN
        IF NEW.grade_100 BETWEEN 87 AND 100 THEN
            SET NEW.grade_5 = 'отлично';
        ELSEIF NEW.grade_100 BETWEEN 73 AND 86 THEN
            SET NEW.grade_5 = 'хорошо';
        ELSEIF NEW.grade_100 BETWEEN 50 AND 72 THEN
            SET NEW.grade_5 = 'удовлетворительно';
        ELSE
            SET NEW.grade_5 = 'неудовлетворительно';
        END IF;
    END IF;
    SET NEW.grade_date = CURDATE();
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER after_delete_user
AFTER DELETE ON User
FOR EACH ROW
BEGIN
    -- Установить статус "неактивный" для студента
    UPDATE Student 
    SET full_name = CONCAT(full_name, ' (удалён)'), email = NULL, phone = NULL 
    WHERE student_id = OLD.user_id;

    -- Установить статус "неактивный" для учителя
    UPDATE Teacher 
    SET full_name = CONCAT(full_name, ' (удалён)'), email = NULL, phone = NULL 
    WHERE teacher_id = OLD.user_id;

    -- Удалить секретаря, если он есть
    DELETE FROM Secretary WHERE secretary_id = OLD.user_id;
END//

DELIMITER ;

CREATE VIEW UserView AS
SELECT user_id, login, full_name, email, phone, permissions
FROM User;

INSERT INTO Direction (direction_name, faculty_name) VALUES ('Нераспределённые студенты', 'Факультет Нераспределённых');
SET @unassigned_direction_id = (SELECT direction_id FROM Direction WHERE direction_name = 'Нераспределённые студенты');
INSERT INTO StudentGroup (group_name, direction_id) VALUES ('Нераспределённые студенты', @unassigned_direction_id);
INSERT INTO `user` (`user_id`, `login`, `password_hash`, `full_name`, `email`, `phone`, `permissions`) VALUES (NULL, 'mdt', 'qwe', 'Бунеев Максим Викторович', 'buneev3@gmail.com', '89538451122', '0');
INSERT INTO `discipline` (`discipline_id`, `discipline_name`, `department_location`) VALUES (NULL, 'Физика', '4-341');
INSERT INTO `discipline` (`discipline_id`, `discipline_name`, `department_location`) VALUES (NULL, 'Математика', '5-123');
INSERT INTO `user` (`user_id`, `login`, `password_hash`, `full_name`, `email`, `phone`, `permissions`) VALUES (NULL, 'derev', 'qwe', 'Деревяшкин Олег Петрович', 'der32@mail.ru', '89653428534', '1');
INSERT INTO `teacherdiscipline` (`teacher_id`, `discipline_id`) VALUES ('2', '1');
INSERT INTO `grades` (`semester`, `student_id`, `teacher_id`, `discipline_id`, `exam_type`, `grade_100`, `grade_5`, `grade_date`) VALUES ('1', '1', '2', '1', 'зачёт', '54', NULL, NULL);
INSERT INTO `user` (`user_id`, `login`, `password_hash`, `full_name`, `email`, `phone`, `permissions`) VALUES (NULL, 'oleg', 'qwe', 'Петров Александр Петрович ', 'oleg23@gmail.com', '89534758234', '1');
CREATE USER 'view_user'@'%' IDENTIFIED VIA mysql_native_password USING '***';GRANT USAGE ON *.* TO 'view_user'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
GRANT SELECT (`user_id`, `login`, `password_hash`, `permissions`) ON `gradestudent`.`user` TO 'view_user'@'%';
CREATE USER 'student_user'@'%' IDENTIFIED VIA mysql_native_password USING '***';GRANT USAGE ON *.* TO 'student_user'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
CREATE USER 'teacher_user'@'%' IDENTIFIED VIA mysql_native_password USING '***';GRANT USAGE ON *.* TO 'teacher_user'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES PER HOUR 0 MAX_USER_CONNECTIONS 0;
CREATE USER 'secretary_user'@'%' IDENTIFIED VIA mysql_native_password USING '***';GRANT USAGE ON *.* TO 'secretary_user'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;GRANT ALL PRIVILEGES ON `gradestudent`.* TO 'secretary_user'@'%';
