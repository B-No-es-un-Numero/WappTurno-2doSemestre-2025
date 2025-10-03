CREATE DATABASE whapp_turno;
USE whapp_turno;

CREATE TABLE Users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    phone_number BIGINT UNIQUE,
    dni BIGINT UNIQUE,
    date_of_birth DATE,
    enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE Doctors (
    user_id VARCHAR(36) PRIMARY KEY,
    specialty VARCHAR(100) NOT NULL,
    accepts_medical_insurance BOOLEAN NOT NULL,
    license_number INT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Availability (
    id VARCHAR(36) PRIMARY KEY,
    doctor_id VARCHAR(36) NOT NULL,
    time_frame VARCHAR(20) NOT NULL,
    days VARCHAR(20) NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(user_id) ON DELETE CASCADE
);

CREATE TABLE Medical_consultations (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL
);

CREATE TABLE Appointments (
    id VARCHAR(36) PRIMARY KEY,
    date_and_time TIMESTAMP NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    doctor_id VARCHAR(36) NOT NULL,
    medical_consultation_id VARCHAR(36) NOT NULL,
    frequency VARCHAR(50),
    state VARCHAR(20) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (medical_consultation_id) REFERENCES Medical_consultations(id) ON DELETE CASCADE
);


INSERT INTO Medical_consultations (id, name, code) VALUES
(UUID(), 'Médico de cabecera — consulta básica', '101001'),
(UUID(), 'Médico de cabecera — visita domiciliaria', '101002'),
(UUID(), 'Consulta en especialidad ambulatoria', '1030xx'),
(UUID(), 'Atención en guardia / urgencia ambulatoria', '1050xx'),
(UUID(), 'Radiografía simple', '3403xx'),
(UUID(), 'Tomografía (TC)', '3410xx'),
(UUID(), 'Resonancia magnética (RM)', '3420xx'),
(UUID(), 'Laboratorio — análisis bioquímico (hemograma)', '6600xx'),
(UUID(), 'Laboratorio — otros análisis (orina, urocultivo)', '66xxxx'),
(UUID(), 'Curaciones', '1070xx'),
(UUID(), 'Electrocardiograma (ECG)', '3040xx'),
(UUID(), 'Ecografía (ultrasonido)', '3430xx');