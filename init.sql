DELETE FROM categories;
DELETE FROM diets;

INSERT INTO diets (name) VALUES ('vegaaninen');
INSERT INTO diets (name) VALUES ('kasvisruoka');
INSERT INTO diets (name) VALUES ('laktoositon');
INSERT INTO diets (name) VALUES ('gluteeniton');

INSERT INTO categories (name) VALUES ('alkuruoka');
INSERT INTO categories (name) VALUES ('pääruoka');
INSERT INTO categories (name) VALUES ('jälkiruoka');
INSERT INTO categories (name) VALUES ('juoma');