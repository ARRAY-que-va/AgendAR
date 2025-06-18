INSERT INTO especialidades (nombre) VALUES
('Cardiología'),
('Pediatría'),
('Dermatología'),
('Odontología'),
('Clínica Médica');


INSERT INTO consultorio (piso, área, sala) VALUES
(1, 'Ala A', 101),
(1, 'Ala B', 102),
(2, 'Ala C', 201),
(2, 'Ala D', 202);


INSERT INTO obrasocial (nombre) VALUES
('OSDE'),
('Galeno'),
('Swiss Medical'),
('PAMI');


INSERT INTO user (usuario, pwd, rol) VALUES
('paciente_ejemplo', 'passpaciente', 'paciente'),
('medico_ejemplo', 'passmedico', 'medico'),
('admin_ejemplo', 'passadmin', 'admin'),
('maria.g', 'mariapass', 'paciente'),
('dr.rodriguez', 'rodriguezpass', 'medico');

INSERT INTO pacientes (nombre, apellido, user_id, dni, fecha_nacimiento, telefono, email, obrasocial_id, direccion) VALUES
('Juan', 'Pérez', (SELECT id_user FROM user WHERE usuario = 'paciente_ejemplo'), '12345678A', '1990-05-15', '1122334455', 'juan.perez@example.com', (SELECT id_obrasocial FROM obrasocial WHERE nombre = 'OSDE'), 'Av. Libertador 123'),
('María', 'García', (SELECT id_user FROM user WHERE usuario = 'maria.g'), '87654321B', '1988-08-22', '1199887766', 'maria.g@example.com', (SELECT id_obrasocial FROM obrasocial WHERE nombre = 'Galeno'), 'Calle Falsa 456');


INSERT INTO medicos (user_id, nombre, apellido, matricula, especialidad_id, fecha_nacimiento, consultorio_id) VALUES
((SELECT id_user FROM user WHERE usuario = 'medico_ejemplo'), 'Carlos', 'González', 'MG98765', (SELECT id_especialidad FROM especialidades WHERE nombre = 'Cardiología'), '1970-03-01', (SELECT id_consultorio FROM consultorio WHERE piso = 1 AND área = 'Ala A' AND sala = 101)),
((SELECT id_user FROM user WHERE usuario = 'dr.rodriguez'), 'Ana', 'Rodríguez', 'AR12345', (SELECT id_especialidad FROM especialidades WHERE nombre = 'Pediatría'), '1982-11-10', (SELECT id_consultorio FROM consultorio WHERE piso = 2 AND área = 'Ala C' AND sala = 201));

-- Insertar turnos (referenciando paciente_id y medico_id)
-- Asegúrate de que las fechas y horas no se superpongan para el mismo médico.
INSERT INTO turnos (paciente_id, medico_id, fecha, hora, estado) VALUES
((SELECT id_paciente FROM pacientes WHERE dni = '12345678A'), (SELECT id_medico FROM medicos WHERE matricula = 'MG98765'), '2025-07-20', '09:00:00', 'reservado'),
((SELECT id_paciente FROM pacientes WHERE dni = '87654321B'), (SELECT id_medico FROM medicos WHERE matricula = 'AR12345'), '2025-07-21', '14:30:00', 'reservado'),
((SELECT id_paciente FROM pacientes WHERE dni = '12345678A'), (SELECT id_medico FROM medicos WHERE matricula = 'AR12345'), '2025-07-21', '15:00:00', 'reservado'); -- Otro turno para el mismo paciente, diferente médico