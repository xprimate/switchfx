DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS forex_thread;
DROP TABLE IF EXISTS forex_thread_post;

CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_name` UNIQUE NOT NULL,
  `first_name` NOT NULL, 
  `last_name`,
  `email` UNIQUE NOT NULL,
  `password` NOT NULL,
  `created_on`,
  `updated_on`,
  `last_activity`,              
  `status`,
  `user_status`,
  `ip`
);

CREATE TABLE `forex_thread` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` NOT NULL,
  `base_currency` NOT NULL,
  `quote_currency` NOT NULL,
  `amount` REAL NOT NULL,
  `exchange_rate` REAL NOT NULL,
  'exchange_rate_cury' NOT NULL,
  'base_exchange' NOT NULL,
  `payment_method` NOT NULL,
  `comment`,
  `ip`,
  `user_name` NOT NULL,
  `status`,
  `created_on`,
  `updated_on`,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
);

CREATE TABLE `forex_thread_post` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `content`,
  `thread_id`,
  `created_on`,
  `user_id`,
  `status`,
  `ip`,
  FOREIGN KEY (`thread_id`) REFERENCES `forex_thread`(`id`)
);

