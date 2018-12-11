--
-- WARNING: before running this script confirm that the foreign key names in the ALTER TABLE
-- statement are correct before executing this script.
--

-- Drop heritage_site_jurisdiction foreign keys (and constraints)
ALTER TABLE heritage_site_jurisdiction
            DROP FOREIGN KEY heritage_site_jurisdiction_ibfk_1,
            DROP FOREIGN KEY heritage_site_jurisdiction_ibfk_2;

ALTER TABLE heritage_site_jurisdiction
            ADD CONSTRAINT heritage_site_fk_heritage_site_id
                           FOREIGN KEY (heritage_site_id)
                           REFERENCES heritage_site(heritage_site_id)
                           ON DELETE CASCADE ON UPDATE CASCADE,
            ADD CONSTRAINT country_area_fk_country_area_id
                           FOREIGN KEY (country_area_id)
                           REFERENCES country_area(country_area_id)
                           ON DELETE CASCADE ON UPDATE CASCADE;