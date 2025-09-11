CREATE DATABASE whapp_turno;
USE whapp_turno;

CREATE TABLE Users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
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
    start_of_time TIME NOT NULL,
    end_of_time TIME NOT NULL,
    days VARCHAR(100) NOT NULL,
    license_number INT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE MedicalConsultations (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

CREATE TABLE Appointments (
    id VARCHAR(50) PRIMARY KEY,
    date_and_time TIMESTAMP NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    doctor_id VARCHAR(50) NOT NULL,
    medical_consultation_id VARCHAR(50) NOT NULL,
    frequency VARCHAR(50),
    state VARCHAR(50) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (medical_consultation_id) REFERENCES MedicalConsultations(id) ON DELETE CASCADE
);

CREATE TABLE ChatMessages (
    id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    doctor_id VARCHAR(50) NOT NULL,
    appointment_id VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    date_and_time TIMESTAMP NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(id) ON DELETE CASCADE
);
