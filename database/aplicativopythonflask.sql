-- Remove o banco de dados se ele já existir
DROP DATABASE IF EXISTS aplicativopythonflask;

-- Cria um novo banco de dados com codificação UTF-8
CREATE DATABASE aplicativopythonflask
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

-- Seleciona o banco de dados recém-criado para uso
USE aplicativopythonflask;

-- Cria a tabela de tarefas com as colunas especificadas
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT, -- Identificador único da tarefa, auto-incrementado
    task_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e hora da criação da tarefa, padrão para o momento atual
    task_title VARCHAR(127) NOT NULL, -- Título da tarefa, não pode ser nulo
    task_description TEXT NOT NULL, -- Descrição da tarefa, não pode ser nula
    task_status ENUM('concluido', 'pendente', 'del') DEFAULT 'pendente' -- Status da tarefa, padrão é 'pendente'
);

-- Seleciona todas as tarefas da tabela (não retornará resultados, pois a tabela está vazia após a criação)
SELECT * FROM tasks;
