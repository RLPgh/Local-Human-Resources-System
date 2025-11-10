-- Sistema de Gestion de Recursos Humanos
-- Base de datos: dbEmpresa

CREATE DATABASE IF NOT EXISTS dbEmpresa;
USE dbEmpresa;

CREATE TABLE roles (
    id_rol INT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

CREATE TABLE departamentos (
    id_departamento INT PRIMARY KEY AUTO_INCREMENT,
    nombre_dep VARCHAR(50) NOT NULL,
    fk_id_e_gerente INT UNIQUE
);

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre_empleado VARCHAR(80),
    apellido_empleado VARCHAR(80),
    edad INT,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    fecha_contrato DATE,
    salario DECIMAL(10, 2) CHECK (salario >= 0),
    fk_id_rol_e INT,
    fk_id_departamento INT,
    FOREIGN KEY (fk_id_rol_e) REFERENCES roles (id_rol),
    FOREIGN KEY (fk_id_departamento) REFERENCES departamentos (id_departamento) ON DELETE SET NULL
);

ALTER TABLE departamentos
ADD FOREIGN KEY (fk_id_e_gerente) REFERENCES empleados(id_empleado) ON DELETE SET NULL;

CREATE TABLE proyectos (
    id_proyecto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_proyecto VARCHAR(100) NOT NULL,
    descripcion_p VARCHAR(1000),
    fecha_inicio_p DATE
);

CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    contraseña_hash VARCHAR(255) NOT NULL,
    fk_id_rol_u INT NOT NULL,
    fk_id_empleado_u INT UNIQUE NOT NULL,
    FOREIGN KEY (fk_id_rol_u) REFERENCES roles (id_rol),
    FOREIGN KEY (fk_id_empleado_u) REFERENCES empleados (id_empleado) ON DELETE CASCADE
);

CREATE TABLE asignacion_proyectos (
    id_asig_proyecto INT PRIMARY KEY AUTO_INCREMENT,
    fecha_asignacion DATE,
    fk_id_empleado_ap INT,
    fk_id_proyecto_ap INT,
    FOREIGN KEY (fk_id_empleado_ap) REFERENCES empleados (id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_proyecto_ap) REFERENCES proyectos (id_proyecto) ON DELETE CASCADE
);

CREATE TABLE registro_tiempos (
    id_rt INT PRIMARY KEY AUTO_INCREMENT,
    fecha_rt DATE,
    tiempo_rt_horas DECIMAL(4, 2),
    descripcion_tareas VARCHAR(1000),
    fk_id_empleado_rt INT,
    fk_id_proyecto_rt INT,
    FOREIGN KEY (fk_id_empleado_rt) REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_proyecto_rt) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
);

ALTER TABLE empleados AUTO_INCREMENT = 1000;
ALTER TABLE usuarios AUTO_INCREMENT = 20000;
ALTER TABLE proyectos AUTO_INCREMENT = 10;
ALTER TABLE asignacion_proyectos AUTO_INCREMENT = 30000;
ALTER TABLE registro_tiempos AUTO_INCREMENT = 100000;

INSERT INTO roles (id_rol, nombre_rol) VALUES (100, 'AdministradorRH');
INSERT INTO roles (id_rol, nombre_rol) VALUES (101, 'Gerente');
INSERT INTO roles (id_rol, nombre_rol) VALUES (102, 'Empleado');
