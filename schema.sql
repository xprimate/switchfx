DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS forex_thread;
DROP TABLE IF EXISTS forex_thread_post;

CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_name` TEXT(100) UNIQUE NOT NULL,
  `first_name` TEXT(100), 
  `last_name` TEXT(100),
  `email` TEXT(254) UNIQUE NOT NULL,
  `password` TEXT(100),
  `created_on` TIMESTAMP,
  `updated_on` TIMESTAMP,
  `last_activity` TIMESTAMP,
  `status` TEXT(100),
  `user_status` TEXT(50),
  `ip` INTEGER
);

CREATE TABLE `forex_thread` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INTEGER,
  `base_currency` TEXT(100),
  `quote_currency` TEXT(100),
  `amount` DECIMAL NOT NULL,
  `exchange_rate` DECIMAL NOT NULL,
  `payment_method` TEXT(50),
  `comment` TEXT(100),
  `ip` INTEGER,
  `user_name` TEXT(100) NOT NULL,
  `status` TEXT(100),
  `created_on` timestamp,
  `updated_on` timestamp,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
);

CREATE TABLE `forex_thread_post` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `content` TEXT(100),
  `thread_id` INTEGER,
  `created_on` timestamp,
  `user_id` INTEGER,
  `status` TEXT(50),
  `ip` INTEGER,
  FOREIGN KEY (`thread_id`) REFERENCES `forex_thread`(`id`)
);

