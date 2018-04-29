---> 138projectstuff is whatever you called the database <---
---> INDEX's might be unique to implementation or database <---

drop database if exists 138projectstuff;
create database 138projectstuff;
use 138projectstuff;

CREATE TABLE market_currency (
'currency_name' VARCHAR(100) NOT NULL,
'currency_type' VARCHAR(2) NOT NULL,
'converted_currency_id' VARCHAR(100) NULL DEFAULT NULL,
PRIMARY KEY ('currency_name'),
INDEX 'market_currency_converted_currency_i_f661515b_fk_market_cu' ('converted_currency_id' ASC),
CONSTRAINT 'market_currency_converted_currency_i_f661515b_fk_market_cu'
FOREIGN KEY ('converted_currency_id')
REFERENCES '138projectstuff'.'market_currency' ('currency_name'))


CREATE TABLE market_user (
'user_id' INT(11) NOT NULL AUTO_INCREMENT,
'email' VARCHAR(254) NOT NULL,
'phone_number' VARCHAR(12) NOT NULL,
'name' VARCHAR(100) NOT NULL,
'address' VARCHAR(300) NOT NULL,
'user_type' VARCHAR(2) NOT NULL,
PRIMARY KEY ('user_id'),
UNIQUE INDEX 'email' ('email' ASC))


CREATE TABLE market_paymentsource (
'payment_source_id' INT(11) NOT NULL AUTO_INCREMENT,
'name' VARCHAR(100) NOT NULL,
'created_on' VARCHAR(20) NOT NULL,
'user_id' INT(11) NOT NULL,
PRIMARY KEY ('payment_source_id'),
INDEX 'market_paymentsource_user_id_b2300da1_fk_market_user_user_id' ('user_id' ASC),
CONSTRAINT 'market_paymentsource_user_id_b2300da1_fk_market_user_user_id'
FOREIGN KEY ('user_id')
REFERENCES '138projectstuff'.'market_user' ('user_id'))


CREATE TABLE market_debitcard (
'id' INT(11) NOT NULL AUTO_INCREMENT,
'bank_name' VARCHAR(100) NOT NULL,
'card_number' VARCHAR(19) NOT NULL,
'name' VARCHAR(100) NOT NULL,
'payment_source_id' INT(11) NOT NULL,
PRIMARY KEY ('id'),
UNIQUE INDEX 'market_debitcard_card_number_b1f7749c_uniq' ('card_number' ASC),
UNIQUE INDEX 'market_debitcard_payment_source_id_4fe7c7e5_uniq' ('payment_source_id' ASC),
CONSTRAINT 'market_debitcard_payment_source_id_4fe7c7e5_fk_market_pa'
FOREIGN KEY ('payment_source_id')
REFERENCES '138projectstuff'.'market_paymentsource' ('payment_source_id'))


CREATE TABLE market_wallet (
'id' INT(11) NOT NULL AUTO_INCREMENT,
'payment_source_id' INT(11) NOT NULL,
PRIMARY KEY ('id'),
UNIQUE INDEX 'market_wallet_payment_source_id_fd0aa08b_uniq' ('payment_source_id' ASC),
CONSTRAINT 'market_wallet_payment_source_id_fd0aa08b_fk_market_pa'
FOREIGN KEY ('payment_source_id')
REFERENCES '138projectstuff'.'market_paymentsource' ('payment_source_id'))
