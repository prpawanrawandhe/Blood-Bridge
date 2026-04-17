----- Db structure -----

CREATE DATABASE blood_bridge;

USE blood_bridge;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(20),
    blood_group VARCHAR(10)
);

CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    blood_group VARCHAR(10),
    city VARCHAR(50)
);
use blood_bridge;
ALTER TABLE users ADD COLUMN city VARCHAR(50) DEFAULT 'Unknown';

