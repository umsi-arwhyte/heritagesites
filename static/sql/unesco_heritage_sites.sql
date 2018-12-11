-- Combine UN Statistics Division (UNSD) standard region, sub-regions, intermediate
-- regions and countries or areas codes (M49) with UNESCO World Heritage List.
-- Source: https://unstats.un.org/unsd/methodology/m49/overview/
-- Source: https://whc.unesco.org/en/list/

--
-- Create database
--

-- CREATE DATABASE IF NOT EXISTS unesco_heritage_sites;
-- USE unesco_heritage_sites;

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS region, sub_region, intermediate_region, dev_status, country_area,
  heritage_site, heritage_site_category, heritage_site_jurisdiction;
SET FOREIGN_KEY_CHECKS=1;

--
-- UNSD M49 Regions
--

CREATE TABLE IF NOT EXISTS region
  (
    region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    region_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (region_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO region (region_name) VALUES
  ('Africa'), ('Americas'), ('Asia'), ('Europe'), ('Oceania');

--
-- UNSD M49 sub-regions.
--

CREATE TABLE IF NOT EXISTS sub_region
  (
    sub_region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    sub_region_name VARCHAR(100) NOT NULL UNIQUE,
    region_id INTEGER NOT NULL,
    PRIMARY KEY (sub_region_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id) ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Set FK variables and populate the sub_region table.
SET @fk_africa =
  (
    SELECT region_id
    FROM region
    WHERE region_name = 'Africa'
  );
SET @fk_americas =
  (
    SELECT region_id
    FROM region
    WHERE region_name = 'Americas'
  );
SET @fk_asia =
  (
    SELECT region_id
    FROM region
    WHERE region_name = 'Asia'
  );
SET @fk_europe =
  (
    SELECT region_id
    FROM region
    WHERE region_name = 'Europe'
  );
SET @fk_oceania =
  (
    SELECT region_id
    FROM region
    WHERE region_name = 'Oceania'
  );

INSERT IGNORE INTO sub_region (sub_region_name, region_id) VALUES
  ('Australia and New Zealand', @fk_oceania),
  ('Central Asia', @fk_asia),
  ('Eastern Asia', @fk_asia),
  ('Eastern Europe', @fk_europe),
  ('Latin America and the Caribbean', @fk_americas),
  ('Melanesia', @fk_oceania),
  ('Micronesia', @fk_oceania),
  ('Northern Africa', @fk_africa),
  ('Northern America', @fk_americas),
  ('Northern Europe', @fk_europe),
  ('Polynesia', @fk_oceania),
  ('South-eastern Asia', @fk_asia),
  ('Southern Asia', @fk_asia),
  ('Southern Europe', @fk_europe),
  ('Sub-Saharan Africa', @fk_africa),
  ('Western Asia', @fk_asia),
  ('Western Europe', @fk_europe);

--
-- UNSD M49 intermediate regions.
--

CREATE TABLE IF NOT EXISTS intermediate_region
  (
    intermediate_region_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    intermediate_region_name VARCHAR(100) NOT NULL UNIQUE,
    sub_region_id INTEGER NOT NULL,
    PRIMARY KEY (intermediate_region_id),
    FOREIGN KEY (sub_region_id) REFERENCES sub_region(sub_region_id) ON DELETE RESTRICT
    ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Set FK variables and populate the intermediate_region table.
SET @fk_latin_am_carrib =
  (
    SELECT sub_region_id
    FROM sub_region
    WHERE sub_region_name = 'Latin America and the Caribbean'
  );
SET @fk_north_europe =
  (
    SELECT sub_region_id
    FROM sub_region
    WHERE sub_region_name = 'Northern Europe'
  );
SET @fk_sub_saharan =
  (
    SELECT sub_region_id
    FROM sub_region
    WHERE sub_region_name = 'Sub-Saharan Africa'
  );

INSERT IGNORE INTO intermediate_region (intermediate_region_name, sub_region_id) VALUES
  ('Caribbean', @fk_latin_am_carrib),
  ('Central America', @fk_latin_am_carrib),
  ('Channel Islands', @fk_north_europe),
  ('Eastern Africa', @fk_sub_saharan),
  ('Middle Africa', @fk_sub_saharan),
  ('South America', @fk_latin_am_carrib),
  ('Southern Africa', @fk_sub_saharan),
  ('Western Africa', @fk_sub_saharan);

--
-- UNSD M49 Development status
--

CREATE TABLE IF NOT EXISTS dev_status
  (
    dev_status_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    dev_status_name VARCHAR(25) NOT NULL UNIQUE,
    PRIMARY KEY (dev_status_id)
   )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert dev_status options
INSERT IGNORE INTO dev_status (dev_status_name) VALUES
  ('Developing'), ('Developed');

--
-- UNSD M49 country or areas.
--

-- Temporary target table for UNSD data import
CREATE TEMPORARY TABLE temp_country_area
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    region_name VARCHAR(100) NULL,
    sub_region_name VARCHAR(100) NULL,
    intermediate_region_name VARCHAR(100) NULL,
    country_area_name VARCHAR(100) NOT NULL,
    country_area_m49_code SMALLINT(4) NOT NULL,
    country_area_iso_alpha3_code CHAR(3) NULL,
    country_area_development_status VARCHAR(25),
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/arwhyte/Development/repos/github/arwhyte/python-scripts/assets/un_area_country_codes-m49.csv'
INTO TABLE temp_country_area
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, region_name, sub_region_name, intermediate_region_name, country_area_name, country_area_m49_code,
   country_area_iso_alpha3_code, @dummy, @dummy, @dummy, country_area_development_status)

  SET region_name = IF(region_name = '', NULL, region_name),
  sub_region_name = IF(sub_region_name = '', NULL, sub_region_name),
  intermediate_region_name = IF(intermediate_region_name = '', NULL, intermediate_region_name),
  country_area_m49_code = IF(country_area_m49_code = '', NULL, country_area_m49_code),
  country_area_iso_alpha3_code = IF(country_area_iso_alpha3_code = '', NULL, country_area_iso_alpha3_code),
  country_area_development_status = IF(country_area_development_status = '', NULL, country_area_development_status);

--
-- UNSD M49 countries and areas
--

CREATE TABLE IF NOT EXISTS country_area
  (
    country_area_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    country_area_name VARCHAR(100) NOT NULL UNIQUE,
    region_id INTEGER NULL,
    sub_region_id INTEGER NULL,
    intermediate_region_id INTEGER NULL,
    m49_code SMALLINT(4) NOT NULL,
    iso_alpha3_code CHAR(3) NOT NULL,
    dev_status_id INT NULL,
    PRIMARY KEY (country_area_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (sub_region_id) REFERENCES sub_region(sub_region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (intermediate_region_id) REFERENCES intermediate_region(intermediate_region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (dev_status_id) REFERENCES dev_status(dev_status_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
   )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert country_area attributes only (N=249) from temp table (no regions).
INSERT IGNORE INTO country_area
  (
    country_area_name,
    region_id,
    sub_region_id,
    intermediate_region_id,
    m49_code,
    iso_alpha3_code,
    dev_status_id
  )
SELECT tc.country_area_name, r.region_id, sr.sub_region_id, ir.intermediate_region_id,
       tc.country_area_m49_code, tc.country_area_iso_alpha3_code, ds.dev_status_id
  FROM temp_country_area tc
       LEFT JOIN region r
              ON tc.region_name = r.region_name
       LEFT JOIN sub_region sr
              ON tc.sub_region_name = sr.sub_region_name
       LEFT JOIN intermediate_region ir
              ON tc.intermediate_region_name = ir.intermediate_region_name
       LEFT JOIN dev_status ds
              ON tc.country_area_development_status = ds.dev_status_name
 WHERE IFNULL(tc.region_name, 0) = IFNULL(r.region_name, 0)
   AND IFNULL(tc.sub_region_name, 0) = IFNULL(sr.sub_region_name, 0)
   AND IFNULL(tc.intermediate_region_name, 0) = IFNULL(ir.intermediate_region_name, 0)
   AND IFNULL(tc.country_area_development_status, 0) = IFNULL(ds.dev_status_name, 0)
 ORDER BY tc.country_area_name;

DROP TEMPORARY TABLE temp_country_area;

--
-- UNESCO heritage site data.
--

-- UNESCO site categories
CREATE TABLE IF NOT EXISTS heritage_site_category
  (
     category_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
     category_name VARCHAR(25) NOT NULL UNIQUE,
     PRIMARY KEY (category_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO heritage_site_category (category_name) VALUES
  ('Cultural'), ('Natural'), ('Mixed');

--
-- Target table for UNESCO heritage sites.
-- WARN: certain UNESCO sites are linked to multiple states.  Handle these entries separately.
-- WARN: this import limited to sites located with a single jurisdiction (transboundary = 0)
--

CREATE TEMPORARY TABLE temp_heritage_site
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    site_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    justification TEXT NULL,
    date_inscribed CHAR(4) NOT NULL,
    longitude VARCHAR(50) NOT NULL,
    -- longitude DECIMAL(11, 8) NOT NULL,
    latitude VARCHAR(50) NOT NULL,
    -- latitude DECIMAL(10, 8) NOT NULL,
    area_hectares VARCHAR(50) NULL,
    -- area_hectares FLOAT NULL,
    category VARCHAR(25) NOT NULL,
    country_area VARCHAR(255) NOT NULL,
    transboundary TINYINT NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Load UNESCO data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE '/Users/arwhyte/Development/repos/github/arwhyte/python-scripts/assets/unesco_heritage_sites.csv'
INTO TABLE temp_heritage_site
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  -- LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (@dummy, @dummy, @dummy, site_name, description, justification, date_inscribed, @dummy,
   @dummy, longitude, latitude, area_hectares, category, @dummy, country_area, @dummy,
   @dummy, @dummy, transboundary);

CREATE TABLE IF NOT EXISTS heritage_site
  (
    heritage_site_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    site_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    justification TEXT NULL,
    date_inscribed YEAR(4) NULL,
    longitude DECIMAL(11, 8) NULL,
    latitude DECIMAL(10, 8) NULL,
    area_hectares DOUBLE NULL,
    heritage_site_category_id INTEGER NOT NULL,
    transboundary TINYINT NOT NULL,
    PRIMARY KEY (heritage_site_id),
    FOREIGN KEY (heritage_site_category_id) REFERENCES heritage_site_category(category_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO heritage_site (site_name, description, justification, date_inscribed,
       longitude, latitude, area_hectares, heritage_site_category_id, transboundary)
SELECT ths.site_name,
       ths.description,
       ths.justification,
       ths.date_inscribed,
       CAST(ths.longitude AS DECIMAL(11, 8)) AS longitude,
       CAST(ths.latitude AS DECIMAL(10, 8)) AS latitude,
       ths.area_hectares + 0.0,
       hsc.category_id,
       ths.transboundary
  FROM temp_heritage_site ths
       LEFT JOIN heritage_site_category hsc
              ON ths.category = hsc.category_name
 ORDER BY ths.id;

--
-- Link UNSD country_area to UNESCO heritage_site
-- WARN: 'Old City of Jerusalem and its Walls' site is NOT associated with a UNSD M49 country_area.
--

-- Junction table linking heritage sites to states (many-to-many).
-- WARN: Django 2.x ORM does not recognize compound keys. Add otherwise superfluous primary key
-- to accommodate a weak ORM.

-- WARN: if a heritage_site record or country_area record is deleted the ON DELETE CASCADE
-- will delete associated records in this junction/associative table.

CREATE TABLE IF NOT EXISTS heritage_site_jurisdiction
  (
    heritage_site_jurisdiction_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    heritage_site_id INTEGER NOT NULL,
    country_area_id INTEGER NOT NULL,
    PRIMARY KEY (heritage_site_jurisdiction_id),
    FOREIGN KEY (heritage_site_id) REFERENCES heritage_site(heritage_site_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (country_area_id) REFERENCES country_area(country_area_id)
    ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Create temporary numbers table that will be used to split out comma-delimited lists of states.
CREATE TEMPORARY TABLE numbers
  (
    num INTEGER NOT NULL UNIQUE,
    PRIMARY KEY (num)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO numbers (num) VALUES
  (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15);

-- Create temporary table to store split out states.
CREATE TEMPORARY TABLE multi_jurisdiction
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    site_name VARCHAR(255) NOT NULL,
    country_area_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- This query splits the states and inserts them into the target temp table.
INSERT IGNORE INTO multi_jurisdiction (site_name, country_area_name)
SELECT ths.site_name,
       SUBSTRING_INDEX(SUBSTRING_INDEX(ths.country_area, ',', numbers.num), ',', -1)
       AS country_area_name
  FROM numbers
       INNER JOIN temp_heritage_site ths
               ON CHAR_LENGTH(ths.country_area) -
                  CHAR_LENGTH(REPLACE(ths.country_area, ',', ''))
                  >= numbers.num - 1
 ORDER BY ths.id, numbers.num;

DROP TEMPORARY TABLE numbers;

-- Insert UNESCO heritage sites linked to multiple states in junction table.
INSERT IGNORE INTO heritage_site_jurisdiction (heritage_site_id, country_area_id)
SELECT hs.heritage_site_id,
       ca.country_area_id
  FROM multi_jurisdiction ms
       LEFT JOIN heritage_site hs
              ON ms.site_name = hs.site_name
       LEFT JOIN country_area ca
              ON ms.country_area_name = ca.country_area_name
 ORDER BY ms.id;

DROP TEMPORARY TABLE temp_heritage_site, multi_jurisdiction;