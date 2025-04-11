CREATE DATABASE IF NOT EXISTS employees;
USE employees;
CREATE TABLE IF NOT EXISTS employee (
  emp_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  primary_skill VARCHAR(50),
  location VARCHAR(50)
);
INSERT INTO employee (emp_id, first_name, last_name, primary_skill, location)
VALUES (1, 'Saeed', 'Goat', 'Kubernetes', 'Toronto');
