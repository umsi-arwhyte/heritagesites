-- Move regional information out of unesco_heritage_sites.country_area to
-- new location table and then update country_area.location_id

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS planet, location;
SET FOREIGN_KEY_CHECKS=1;

--
-- UNSD Global "World".  Add Earth/World to give Antarctica a parent location.
-- WARNING: "Global" is a MySQL reserved word so we can't use UNSD term.

CREATE TABLE IF NOT EXISTS planet
  (
    planet_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    planet_name VARCHAR(50) NOT NULL UNIQUE,
    unsd_name VARCHAR(50) NULL,
    PRIMARY KEY (planet_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Insert "Earth/World"
INSERT IGNORE INTO planet (planet_name, unsd_name) VALUES ('Earth', 'World');

--
-- UNSD region. Add region.planet_id (FK)
--

ALTER TABLE region
        ADD COLUMN planet_id INT NOT NULL DEFAULT 1,
        ADD CONSTRAINT region_fk_planet_id
            FOREIGN KEY (planet_id) REFERENCES planet(planet_id)
            ON DELETE RESTRICT ON UPDATE CASCADE;

--  Update all regions with "World" parent (planet_id = 1)
UPDATE region r
   SET r.planet_id = 1;

--
-- Non-recursive approach to storing UNSD planet, region, sub_region,
-- intermediate_region combinations. country_area.location_id will be added
--

CREATE TABLE IF NOT EXISTS location
  (
    location_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    planet_id INTEGER NOT NULL,
    region_id INTEGER NULL,
    sub_region_id INTEGER NULL,
    intermediate_region_id INTEGER NULL,
    PRIMARY KEY (location_id),
    FOREIGN KEY (planet_id) REFERENCES planet(planet_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (region_id) REFERENCES region(region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (sub_region_id) REFERENCES sub_region(sub_region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (intermediate_region_id) REFERENCES intermediate_region(intermediate_region_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
   )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

-- Next insert locations drawn from country_area (includes Antarctica).
INSERT IGNORE INTO location
       (
         planet_id,
         region_id,
         sub_region_id,
         intermediate_region_id
       )
SELECT 1 AS planet_id, region_id, sub_region_id, intermediate_region_id
  FROM country_area
 GROUP BY planet_id, region_id, sub_region_id, intermediate_region_id
 ORDER BY planet_id, region_id, sub_region_id, intermediate_region_id;

--
-- UNSD country_area. Add country_area.location_id (FK)
--

ALTER TABLE country_area
        ADD COLUMN location_id INT NOT NULL DEFAULT 1 AFTER iso_alpha3_code,
        ADD CONSTRAINT country_area_fk_location_id
            FOREIGN KEY (location_id) REFERENCES location(location_id)
            ON DELETE RESTRICT ON UPDATE CASCADE;

-- Second, update country_area.location_id based on matching location.location_id region values.
UPDATE country_area ca
   SET ca.location_id = (
       SELECT l.location_id
         FROM location l
        WHERE l.planet_id = 1
          AND IFNULL(l.region_id, 0) = IFNULL(ca.region_id, 0)
          AND IFNULL(l.sub_region_id, 0) = IFNULL(ca.sub_region_id, 0)
          AND IFNULL(l.intermediate_region_id, 0) = IFNULL(ca.intermediate_region_id, 0)
       );
