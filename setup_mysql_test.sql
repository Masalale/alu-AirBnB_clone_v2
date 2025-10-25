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

-- 7) Create states, cities, amenities, places, reviews tables
USE `hbnb_dev_db`;
CREATE TABLE IF NOT EXISTS `states` (
	`id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `cities` (
	`id` VARCHAR(60) NOT NULL,
	`state_id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`state_id`) REFERENCES `states`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `amenities` (
	`id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `places` (
	`id` VARCHAR(60) NOT NULL,
	`city_id` VARCHAR(60) NOT NULL,
	`user_id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`description` TEXT DEFAULT NULL,
	`number_rooms` INT DEFAULT 0,
	`number_bathrooms` INT DEFAULT 0,
	`max_guest` INT DEFAULT 0,
	`price_by_night` INT DEFAULT 0,
	`latitude` FLOAT DEFAULT NULL,
	`longitude` FLOAT DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`city_id`) REFERENCES `cities`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `reviews` (
	`id` VARCHAR(60) NOT NULL,
	`place_id` VARCHAR(60) NOT NULL,
	`user_id` VARCHAR(60) NOT NULL,
	`text` TEXT DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`place_id`) REFERENCES `places`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `place_amenity` (
	`place_id` VARCHAR(60) NOT NULL,
	`amenity_id` VARCHAR(60) NOT NULL,
	PRIMARY KEY (`place_id`,`amenity_id`),
	FOREIGN KEY (`place_id`) REFERENCES `places`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`amenity_id`) REFERENCES `amenities`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

USE `hbnb_test_db`;
-- duplicate schema in test DB
CREATE TABLE IF NOT EXISTS `states` (
	`id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `cities` (
	`id` VARCHAR(60) NOT NULL,
	`state_id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`state_id`) REFERENCES `states`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `amenities` (
	`id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `places` (
	`id` VARCHAR(60) NOT NULL,
	`city_id` VARCHAR(60) NOT NULL,
	`user_id` VARCHAR(60) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`description` TEXT DEFAULT NULL,
	`number_rooms` INT DEFAULT 0,
	`number_bathrooms` INT DEFAULT 0,
	`max_guest` INT DEFAULT 0,
	`price_by_night` INT DEFAULT 0,
	`latitude` FLOAT DEFAULT NULL,
	`longitude` FLOAT DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`city_id`) REFERENCES `cities`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `reviews` (
	`id` VARCHAR(60) NOT NULL,
	`place_id` VARCHAR(60) NOT NULL,
	`user_id` VARCHAR(60) NOT NULL,
	`text` TEXT DEFAULT NULL,
	`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`place_id`) REFERENCES `places`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `place_amenity` (
	`place_id` VARCHAR(60) NOT NULL,
	`amenity_id` VARCHAR(60) NOT NULL,
	PRIMARY KEY (`place_id`,`amenity_id`),
	FOREIGN KEY (`place_id`) REFERENCES `places`(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`amenity_id`) REFERENCES `amenities`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
