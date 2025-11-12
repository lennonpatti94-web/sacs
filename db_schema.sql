CREATE DATABASE IF NOT EXISTS sacs_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sacs_db;

CREATE TABLE IF NOT EXISTS paciente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150),
  telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS profissional (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(150),
  especialidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS consulta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT,
  profissional_id INT,
  data_hora DATETIME,
  status ENUM('agendada','confirmada','cancelada') DEFAULT 'agendada',
  FOREIGN KEY (paciente_id) REFERENCES paciente(id),
  FOREIGN KEY (profissional_id) REFERENCES profissional(id)
);
