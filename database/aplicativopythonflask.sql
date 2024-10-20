DROP DATABASE IF EXISTS aplicativopythonflask;

CREATE DATABASE aplicativopythonflask
	character set utf8mb4
    collate utf8mb4_general_ci;
    
USE aplicativopythonflask;

CREATE TABLE tasks (
	task_id INT PRIMARY KEY AUTO_INCREMENT,
    task_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_title VARCHAR(127) NOT NULL,
    task_description TEXT NOT NULL,
    task_status ENUM('concluido', 'pendente', 'del') DEFAULT 'pendente'
);

 

SELECT * FROM tasks;