CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS user_services (
    service_name VARCHAR(100) PRIMARY KEY,
    cms_type VARCHAR(15),
    cms_db_user VARCHAR(20),
    cms_db_password VARCHAR(15),
    cms_root_password VARCHAR(15),
    ip VARCHAR(15),
    puerto INT(8),
    state VARCHAR(10),
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);

-- CREATE TABLE IF NOT EXISTS user_services (
--     service_id INT PRIMARY KEY,
--     service_name VARCHAR(100),
--     username VARCHAR(50),
--     FOREIGN KEY (username) REFERENCES users(username)
-- );

CREATE TABLE IF NOT EXISTS user_kvm (
    kvm_name VARCHAR(50) PRIMARY KEY,
    kvm_memory VARCHAR(10),
    kvm_cpus VARCHAR(10),
    kvm_iso VARCHAR(100),
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);


CREATE TABLE IF NOT EXISTS user_databases (
    database_name VARCHAR(100) PRIMARY KEY,
    database_type VARCHAR(15),
    db_user VARCHAR(20),
    db_password VARCHAR(15),
    root_password VARCHAR(15),
    ip VARCHAR(15),
    puerto INT(8),
    state VARCHAR(10),
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);