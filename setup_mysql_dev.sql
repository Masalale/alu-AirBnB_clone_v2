-- setup_mysql_dev.sql
-- Create database and user for AirBnB clone development environment
-- Idempotent: will not fail if database or user already exists

-- 1) Create the development database if it does not already exist
CREATE DATABASE IF NOT EXISTS `hbnb_dev_db`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2) Create the user if it does not exist and set its password
-- Note: CREATE USER ... IF NOT EXISTS is supported in modern MySQL/MariaDB.
-- If your server is older and does not support IF NOT EXISTS, replace
-- with appropriate user creation/alter commands.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Ensure the user's password is set to the required value (safe to run repeatedly)
ALTER USER 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd' ;

-- 3) Grant privileges on the development database only
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';

-- 4) Ensure the user has SELECT privilege on performance_schema only
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';

-- 5) Apply privilege changes
FLUSH PRIVILEGES;

-- End of setup
