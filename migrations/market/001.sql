BEGIN;
--
-- Create model DebitCard
--
CREATE TABLE `market_debitcard` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `bank_name` varchar(100) NOT NULL, `card_number` varchar(19) NOT NULL, `name` varchar(100) NOT NULL);
--
-- Create model PaymentSource
--
CREATE TABLE `market_paymentsource` (`payment_source_id` varchar(20) NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `created_on` time(6) NOT NULL, `created_at` date NOT NULL);
--
-- Create model Wallet
--
CREATE TABLE `market_wallet` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `payment_source_id` varchar(20) NOT NULL);
--
-- Add field payment_source to debitcard
--
ALTER TABLE `market_debitcard` ADD COLUMN `payment_source_id` varchar(20) NOT NULL;
ALTER TABLE `market_wallet` ADD CONSTRAINT `market_wallet_payment_source_id_fd0aa08b_fk_market_pa` FOREIGN KEY (`payment_source_id`) REFERENCES `market_paymentsource` (`payment_source_id`);
ALTER TABLE `market_debitcard` ADD CONSTRAINT `market_debitcard_payment_source_id_4fe7c7e5_fk_market_pa` FOREIGN KEY (`payment_source_id`) REFERENCES `market_paymentsource` (`payment_source_id`);
COMMIT;
