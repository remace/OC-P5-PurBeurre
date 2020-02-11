CREATE TABLE IF NOT EXISTS `mydb`.`foods` (
  `food_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `food_name` VARCHAR(1000) NOT NULL,
  `ingredients` VARCHAR(1000) NULL,
  `additives` VARCHAR(1000) NULL,
  `nutriscore` CHAR(10) NULL,
  `nutrient` VARCHAR(1000) NULL,
  `label` VARCHAR(1000) NULL,
  `store` VARCHAR(1000) NULL,
  `barcode` BIGINT NULL,
  PRIMARY KEY (`food_id`),
  UNIQUE INDEX `food_id_UNIQUE` (`food_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_id`
    FOREIGN KEY (category_id)
    REFERENCES `mydb`.`categories` (category_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`substitutes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`substitutes` (
  `substitute_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `food_name` VARCHAR(1000) NOT NULL,
  `ingredients` VARCHAR(1000) NULL,
  `additives` VARCHAR(1000) NULL,
  `nutriscore` CHAR(10) NULL,
  `nutrient` VARCHAR(1000) NULL,
  `label` VARCHAR(1000) NULL,
  `store` VARCHAR(1000) NULL,
  `barcode` BIGINT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`substitute_id`),
  CONSTRAINT `fk_category_id`
    FOREIGN KEY (category_id)
    REFERENCES `mydb`.`categories` (category_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    )
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
