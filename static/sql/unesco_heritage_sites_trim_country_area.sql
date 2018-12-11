-- WARNING: before running this script confirm that the foreign key names in the ALTER TABLE
-- statement are correct before executing this script.
--

-- Drop country_area region-related foreign keys and columns
ALTER TABLE country_area
       DROP FOREIGN KEY country_area_ibfk_1,
       DROP COLUMN region_id,
       DROP FOREIGN KEY country_area_ibfk_2,
       DROP COLUMN sub_region_id,
       DROP FOREIGN KEY country_area_ibfk_3,
       DROP COLUMN intermediate_region_id;
