CREATE DATABASE IF NOT EXISTS `VENTE_JEUX` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `VENTE_JEUX`;

/*
CREATE TABLE `CALENDRIER` (
  `id_calendrier` DATE NOT NULL,
  PRIMARY KEY (`id_calendrier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
*/

CREATE TABLE `CONSOLES` (
  `id_console` INT NOT NULL,
  `nom_console` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_console`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `JEUX` (
  `id_jeu` INT NOT NULL,
  `nom_jeu` VARCHAR(200) NOT NULL,
  `na_vente_jeu` FLOAT,
  `eu_vente_jeu` FLOAT,
  `jp_vente_jeu` FLOAT,
  `autre_vente_jeu` FLOAT,
  `global_vente_jeu` FLOAT,
  `id_calendrier` DATE NOT NULL,
  `id_console` INT NOT NULL,
  `id_genre` INT NOT NULL,
  `id_editeur` INT,
  PRIMARY KEY (`id_jeu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `GENRES` (
  `id_genre` INT NOT NULL,
  `nom_genre` VARCHAR(100),
  PRIMARY KEY (`id_genre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `EDITEURS` (
  `id_editeur` INT,
  `nom_editeur` VARCHAR(100),
  PRIMARY KEY (`id_editeur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ALTER TABLE `JEUX` ADD FOREIGN KEY (`id_editeur`) REFERENCES `EDITEURS` (`id_editeur`);
-- ALTER TABLE `JEUX` ADD FOREIGN KEY (`id_genre`) REFERENCES `GENRES` (`id_genre`);
-- ALTER TABLE `JEUX` ADD FOREIGN KEY (`id_console`) REFERENCES `CONSOLES` (`id_console`);
-- ALTER TABLE `JEUX` ADD FOREIGN KEY (`id_calendrier`) REFERENCES `CALENDRIER` (`id_calendrier`);