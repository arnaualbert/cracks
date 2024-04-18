CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS user_services (
    service_id INT PRIMARY KEY,
    service_name VARCHAR(100),
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS user_kvm (
    kvm_nam VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);