-- setup_mysql_test.sql
-- Create development and test databases and a user for AirBnB clone
-- Idempotent: will not fail if database, user, or tables already exist

-- Adjust names as needed by tests: create both hbnb_dev_db and hbnb_test_db

-- 1) Create the development and test databases if they do not already exist
CREATE DATABASE IF NOT EXISTS `hbnb_dev_db`
		DEFAULT CHARACTER SET utf8mb4
		DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS `hbnb_test_db`
		DEFAULT CHARACTER SET utf8mb4
		DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2) Create the user if it does not exist and set its password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
ALTER USER 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd' ;

-- 3) Grant privileges on both databases
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_test'@'localhost';
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';

-- 4) Ensure the user has SELECT privilege on performance_schema (optional)
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';

-- 5) Apply privilege changes
FLUSH PRIVILEGES;

-- 6) Create the users table in both databases if it does not exist
-- The tests expect columns: email, password, first_name, last_name
-- and the table name to be `users` inside the database (hbnb_dev_db)

USE `hbnb_dev_db`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` VARCHAR(60) NOT NULL,
	`email` VARCHAR(128) NOT NULL,
	`password` VARCHAR(128) NOT NULL,
	`first_name` VARCHAR(128) DEFAULT NULL,
	`last_name` VARCHAR(128) DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

USE `hbnb_test_db`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` VARCHAR(60) NOT NULL,
	`email` VARCHAR(128) NOT NULL,
	`password` VARCHAR(128) NOT NULL,
	`first_name` VARCHAR(128) DEFAULT NULL,
	`last_name` VARCHAR(128) DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- End of setup
