CREATE DATABASE inventario_conexion;
USE Inventario_Conexion;

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(100),
  role ENUM('admin','user') NOT NULL
);

CREATE TABLE libros (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(100),
  autor VARCHAR(100),
  cantidad INT
);

-- Usuarios de ejemplo:
INSERT INTO usuarios (email, password, role) VALUES
('admin@empresa.cl', 'admin123', 'admin'),
('user@empresa.cl', 'user123', 'user');
