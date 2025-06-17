CREATE DATABASE IF NOT EXISTS agendar;
USE agendar;

CREATE TABLE especialidades
 (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE consultorio (
    id_consultorio INT AUTO_INCREMENT PRIMARY KEY,
    piso INT NOT NULL,
    área VARCHAR(50) NOT NULL,
    sala INT NOT NULL
);

CREATE TABLE obrasocial (
    id_obrasocial INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE user (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    pwd VARCHAR(20) NOT NULL,
    usuario VARCHAR(20),
    rol ENUM('paciente', 'medico', 'admin') DEFAULT 'paciente'
);

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id_user),
    dni VARCHAR(20) NOT NULL UNIQUE,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    obrasocial_id INT,
    FOREIGN KEY (obrasocial_id) REFERENCES obrasocial(id_obrasocial),
    direccion VARCHAR(100) NOT NULL
);

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id_user),
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    especialidad_id INT NOT NULL,
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id_especialidad),
    fecha_nacimiento DATE,
    consultorio_id INT NOT NULL,
    FOREIGN KEY (consultorio_id) REFERENCES consultorio(id_consultorio)
);

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('reservado', 'atendido', 'cancelado') DEFAULT 'reservado',
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (medico_id) REFERENCES medicos(id_medico),
    UNIQUE (medico_id, fecha, hora)
);
