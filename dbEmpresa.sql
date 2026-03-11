-- Sistema de Gestion de Recursos Humanos
-- Base de datos: dbEmpresa (SQLite)

CREATE TABLE roles (
    id_rol INTEGER PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

CREATE TABLE departamentos (
    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_dep VARCHAR(50) NOT NULL,
    fk_id_e_gerente INTEGER UNIQUE,
    FOREIGN KEY (fk_id_e_gerente) REFERENCES empleados(id_empleado) ON DELETE SET NULL
);

CREATE TABLE empleados (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_empleado VARCHAR(80),
    apellido_empleado VARCHAR(80),
    edad INTEGER,
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    fecha_contrato DATE,
    salario DECIMAL(10, 2) CHECK (salario >= 0),
    fk_id_rol_e INTEGER,
    fk_id_departamento INTEGER,
    FOREIGN KEY (fk_id_rol_e) REFERENCES roles (id_rol),
    FOREIGN KEY (fk_id_departamento) REFERENCES departamentos (id_departamento) ON DELETE SET NULL
);

CREATE TABLE proyectos (
    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_proyecto VARCHAR(100) NOT NULL,
    descripcion_p VARCHAR(1000),
    fecha_inicio_p DATE
);

CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    contraseña_hash VARCHAR(255) NOT NULL,
    fk_id_rol_u INTEGER NOT NULL,
    fk_id_empleado_u INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (fk_id_rol_u) REFERENCES roles (id_rol),
    FOREIGN KEY (fk_id_empleado_u) REFERENCES empleados (id_empleado) ON DELETE CASCADE
);

CREATE TABLE asignacion_proyectos (
    id_asig_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_asignacion DATE,
    fk_id_empleado_ap INTEGER,
    fk_id_proyecto_ap INTEGER,
    FOREIGN KEY (fk_id_empleado_ap) REFERENCES empleados (id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_proyecto_ap) REFERENCES proyectos (id_proyecto) ON DELETE CASCADE
);

CREATE TABLE registro_tiempos (
    id_rt INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_rt DATE,
    tiempo_rt_horas DECIMAL(4, 2),
    descripcion_tareas VARCHAR(1000),
    fk_id_empleado_rt INTEGER,
    fk_id_proyecto_rt INTEGER,
    FOREIGN KEY (fk_id_empleado_rt) REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_proyecto_rt) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE
);

-- SQLite crea la tabla sqlite_sequence automáticamente si hay AUTOINCREMENT, pero a veces no hasta hacer un primer insert
-- Podemos forzar creándola o usando un truco: insertar datos ficticios y borrarlos para inicializar contadores.
INSERT INTO sqlite_sequence (name, seq) VALUES ('empleados', 999);
INSERT INTO sqlite_sequence (name, seq) VALUES ('usuarios', 19999);
INSERT INTO sqlite_sequence (name, seq) VALUES ('proyectos', 9);
INSERT INTO sqlite_sequence (name, seq) VALUES ('asignacion_proyectos', 29999);
INSERT INTO sqlite_sequence (name, seq) VALUES ('registro_tiempos', 99999);

INSERT INTO roles (id_rol, nombre_rol) VALUES (100, 'AdministradorRH');
INSERT INTO roles (id_rol, nombre_rol) VALUES (101, 'Gerente');
INSERT INTO roles (id_rol, nombre_rol) VALUES (102, 'Empleado');
