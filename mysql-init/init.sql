-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : ven. 06 juin 2025 à 16:31
-- Version du serveur : 8.3.0
-- Version de PHP : 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `themaa_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `Formation`
--

CREATE TABLE `Formation` (
  `id_formation` int NOT NULL,
  `nom` varchar(200) DEFAULT NULL,
  `type` enum('initiale','continue') NOT NULL,
  `description` text NOT NULL,
  `duree` varchar(50) NOT NULL,
  `duree_heures` float DEFAULT NULL,
  `dates` varchar(100) NOT NULL,
  `lieu` varchar(200) DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `conditions_acces` text,
  `financement` varchar(255) DEFAULT NULL,
  `presentation_intervenants` text,
  `lien_inscription` varchar(200) DEFAULT NULL,
  `label` varchar(255) DEFAULT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `id_organisme` int NOT NULL,
  `etat` enum('valide','en_attente') NOT NULL DEFAULT 'en_attente',
  `raison` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Formation`
--

INSERT INTO `Formation` (`id_formation`, `nom`, `type`, `description`, `duree`, `duree_heures`, `dates`, `lieu`, `prix`, `conditions_acces`, `financement`, `presentation_intervenants`, `lien_inscription`, `label`, `certifications`, `id_organisme`, `etat`, `raison`) VALUES
(1, 'Diplôme National Supérieur Professionnel de Comédien – Spécialité Acteur-Marionnettiste', 'initiale', 'Formation de 3 ans délivrant le DNSP, axée sur la maîtrise des fondamentaux de la marionnette contemporaine et le développement du langage artistique personnel.', '3 ans', 1800, '05/06/2025 au 12/06/2025', '16 avenue Jean Jaurès, 08000 Charleville-Mézières', NULL, 'Sur concours tous les 3 ans, accessible à partir de 18 ans.', 'OPCO, France Travail, autofinancement', 'Intervenants français et internationaux, artistes et professionnels du spectacle vivant.', 'https://marionnette.com/formation/inscription', 'Qualiopi', 'DNSP', 1, 'valide', NULL),
(2, 'Formation Continue en Théâtre d\'Objets', 'continue', 'Perfectionnement en théâtre d\'objets et manipulation.', '2 semaines', 70, '06/06/2025 au 13/06/2025', '10 Avenue des Champs-Élysées, 75008 Paris', 800.00, 'Expérience en théâtre requise', 'CPF', 'Artistes professionnels du théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 2, 'valide', NULL),
(3, 'Atelier de Création de Marionnettes Géantes', 'initiale', 'Atelier pratique pour apprendre à créer des marionnettes géantes.', '1 semaine', 35, '07/06/2025 au 14/06/2025', '3A Rue du 22 Novembre, 67000 Strasbourg', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 3, 'valide', NULL),
(4, 'Formation en Marionnettes à Fil', 'continue', 'Formation avancée sur les techniques de marionnettes à fil.', '1 mois', 120, '08/06/2025 au 15/06/2025', '103 Rue de Vesle, 51100 Reims', 1200.00, 'Expérience en marionnettes requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 4, 'valide', NULL),
(5, 'Formation Initiale en Théâtre d\'Ombres', 'initiale', 'Introduction aux techniques du théâtre d\'ombres.', '2 semaines', 50, '09/06/2025 au 16/06/2025', '10 Rue Saint-Dizier, 54000 Nancy', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 5, 'valide', NULL),
(6, 'Atelier de Marionnettes Contemporaines', 'continue', 'Atelier pratique pour explorer les techniques contemporaines de marionnettes.', '3 jours', 21, '10/06/2025 au 17/06/2025', '7 Boulevard de l’Europe, 68100 Mulhouse', 300.00, 'Expérience en marionnettes requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 6, 'valide', NULL),
(7, 'Formation en Marionnettes à Gaine', 'initiale', 'Formation complète sur les techniques de marionnettes à gaine.', '2 mois', 150, '11/06/2025 au 18/06/2025', '8 Place de la République, 59000 Lille', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 7, 'valide', NULL),
(8, 'Atelier de Marionnettes Traditionnelles', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles de marionnettes.', '1 semaine', 35, '12/06/2025 au 19/06/2025', '7 Rue des Vergeaux, 80000 Amiens', 400.00, 'Expérience en marionnettes requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 8, 'valide', NULL),
(9, 'Formation Initiale en Arts de la Scène', 'initiale', 'Formation complète sur les arts de la scène et les techniques de marionnettes.', '4 mois', 300, '13/06/2025 au 20/06/2025', '18 Rue des Fontinettes, 62100 Calais', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 9, 'valide', NULL),
(10, 'Formation Continue en Marionnettes Géantes', 'continue', 'Perfectionnement en création et manipulation de marionnettes géantes.', '2 semaines', 70, '14/06/2025 au 21/06/2025', '1 Rue de Lyon, 02100 Saint-Quentin', 800.00, 'Expérience en marionnettes géantes requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 10, 'valide', NULL),
(11, 'Atelier de Théâtre d\'Objets', 'initiale', 'Atelier pratique pour apprendre les techniques de théâtre d\'objets.', '1 semaine', 35, '15/06/2025 au 22/06/2025', '45 bis Rue Jeanne-d’Arc, 76000 Rouen', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans le théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 11, 'valide', NULL),
(12, 'Formation en Marionnettes à Fil Avancées', 'continue', 'Formation avancée sur les techniques de marionnettes à fil.', '1 mois', 120, '16/06/2025 au 23/06/2025', '5 Rue des Boutiques, 14000 Caen', 1200.00, 'Expérience en marionnettes à fil requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 12, 'valide', NULL),
(13, 'Formation Initiale en Théâtre d\'Ombres Avancé', 'initiale', 'Introduction aux techniques avancées du théâtre d\'ombres.', '2 semaines', 50, '17/06/2025 au 24/06/2025', '172 Boulevard de Strasbourg, 76600 Le Havre', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 13, 'valide', NULL),
(14, 'Atelier de Marionnettes Contemporaines Avancées', 'continue', 'Atelier pratique pour explorer les techniques contemporaines avancées de marionnettes.', '3 jours', 21, '18/06/2025 au 25/06/2025', '1 Rue de l’Ancien-Quai, 50100 Cherbourg-en-Cotentin', 300.00, 'Expérience en marionnettes contemporaines requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 14, 'valide', NULL),
(15, 'Formation en Marionnettes à Gaine Avancées', 'initiale', 'Formation complète sur les techniques avancées de marionnettes à gaine.', '2 mois', 150, '19/06/2025 au 26/06/2025', '11 Place Sainte-Anne, 35000 Rennes', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 15, 'valide', NULL),
(16, 'Atelier de Marionnettes Traditionnelles Avancées', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles avancées de marionnettes.', '1 semaine', 35, '20/06/2025 au 27/06/2025', '25 Place de la République, 56000 Vannes', 400.00, 'Expérience en marionnettes traditionnelles requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 16, 'valide', NULL),
(17, 'Formation Initiale en Arts de la Scène Avancés', 'initiale', 'Formation complète sur les arts de la scène avancés et les techniques de marionnettes.', '4 mois', 300, '21/06/2025 au 28/06/2025', '5 Place de la Résistance, 22000 Saint-Brieuc', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 17, 'valide', NULL),
(18, 'Formation Continue en Marionnettes Géantes Avancées', 'continue', 'Perfectionnement en création et manipulation avancées de marionnettes géantes.', '2 semaines', 70, '22/06/2025 au 29/06/2025', '17 Allée des Tanneurs, 44000 Nantes', 800.00, 'Expérience en marionnettes géantes avancées requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 18, 'valide', NULL),
(19, 'Atelier de Théâtre d\'Objets Avancé', 'initiale', 'Atelier pratique pour apprendre les techniques avancées de théâtre d\'objets.', '1 semaine', 35, '23/06/2025 au 30/06/2025', '1 Rue Franklin-Roosevelt, 49100 Angers', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans le théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 19, 'valide', NULL),
(20, 'Formation en Marionnettes à Fil Professionnelles', 'continue', 'Formation professionnelle sur les techniques de marionnettes à fil.', '1 mois', 120, '24/06/2025 au 01/07/2025', '13 Place de la République, 72000 Le Mans', 1200.00, 'Expérience en marionnettes à fil requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 20, 'valide', NULL),
(21, 'Formation Initiale en Théâtre d\'Ombres Professionnel', 'initiale', 'Introduction aux techniques professionnelles du théâtre d\'ombres.', '2 semaines', 50, '25/06/2025 au 02/07/2025', '8 Rue Georges Clemenceau, 85000 La Roche-sur-Yon', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 21, 'valide', NULL),
(22, 'Atelier de Marionnettes Contemporaines Professionnelles', 'continue', 'Atelier pratique pour explorer les techniques contemporaines professionnelles de marionnettes.', '3 jours', 21, '26/06/2025 au 03/07/2025', '10 Place du Châtelet, 45000 Orléans', 300.00, 'Expérience en marionnettes contemporaines requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 22, 'valide', NULL),
(23, 'Formation en Marionnettes à Gaine Professionnelles', 'initiale', 'Formation complète sur les techniques professionnelles de marionnettes à gaine.', '2 mois', 150, '27/06/2025 au 04/07/2025', '1 Boulevard Béranger, 37000 Tours', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 23, 'valide', NULL),
(24, 'Atelier de Marionnettes Traditionnelles Professionnelles', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles professionnelles de marionnettes.', '1 semaine', 35, '28/06/2025 au 05/07/2025', '29 Rue Moyenne, 18000 Bourges', 400.00, 'Expérience en marionnettes traditionnelles requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 24, 'valide', NULL),
(25, 'Formation Initiale en Arts de la Scène Professionnels', 'initiale', 'Formation complète sur les arts de la scène professionnels et les techniques de marionnettes.', '4 mois', 300, '29/06/2025 au 06/07/2025', '26 Boulevard Georges Clemenceau, 21000 Dijon', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 25, 'valide', NULL),
(26, 'Formation Continue en Marionnettes Géantes Professionnelles', 'continue', 'Perfectionnement en création et manipulation professionnelles de marionnettes géantes.', '2 semaines', 70, '30/06/2025 au 07/07/2025', '44 Rue de Belfort, 25000 Besançon', 800.00, 'Expérience en marionnettes géantes professionnelles requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 26, 'valide', NULL),
(27, 'Atelier de Théâtre d\'Objets Professionnel', 'initiale', 'Atelier pratique pour apprendre les techniques professionnelles de théâtre d\'objets.', '1 semaine', 35, '01/07/2025 au 08/07/2025', '25 bis Avenue Pierre-Bérégovoy, 58000 Nevers', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans le théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 27, 'valide', NULL),
(28, 'Formation en Marionnettes à Fil Expert', 'continue', 'Formation experte sur les techniques de marionnettes à fil.', '1 mois', 120, '02/07/2025 au 09/07/2025', '24 Rue de la République, 69002 Lyon', 1200.00, 'Expérience en marionnettes à fil requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 28, 'valide', NULL),
(29, 'Formation Initiale en Théâtre d\'Ombres Expert', 'initiale', 'Introduction aux techniques expertes du théâtre d\'ombres.', '2 semaines', 50, '03/07/2025 au 10/07/2025', '12 Avenue Alsace-Lorraine, 38000 Grenoble', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 29, 'valide', NULL),
(30, 'Atelier de Marionnettes Contemporaines Expert', 'continue', 'Atelier pratique pour explorer les techniques contemporaines expertes de marionnettes.', '3 jours', 21, '04/07/2025 au 11/07/2025', '22 Place de Jaude, 63000 Clermont-Ferrand', 300.00, 'Expérience en marionnettes contemporaines requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 30, 'valide', NULL),
(31, 'Formation en Marionnettes à Gaine Expert', 'initiale', 'Formation complète sur les techniques expertes de marionnettes à gaine.', '2 mois', 150, '05/07/2025 au 12/07/2025', '1 Rue de la Poste, 74000 Annecy', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 31, 'valide', NULL),
(32, 'Atelier de Marionnettes Traditionnelles Expert', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles expertes de marionnettes.', '1 semaine', 35, '06/07/2025 au 13/07/2025', '9 Rue Lafayette, 31000 Toulouse', 400.00, 'Expérience en marionnettes traditionnelles requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 32, 'valide', NULL),
(33, 'Formation Initiale en Arts de la Scène Experts', 'initiale', 'Formation complète sur les arts de la scène experts et les techniques de marionnettes.', '4 mois', 300, '07/07/2025 au 14/07/2025', '33 Rue de la Cavalerie, 34000 Montpellier', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 33, 'valide', NULL),
(34, 'Formation Continue en Marionnettes Géantes Experts', 'continue', 'Perfectionnement en création et manipulation expertes de marionnettes géantes.', '2 semaines', 70, '08/07/2025 au 15/07/2025', '19 Boulevard Georges Clemenceau, 66000 Perpignan', 800.00, 'Expérience en marionnettes géantes expertes requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 34, 'valide', NULL),
(35, 'Atelier de Théâtre d\'Objets Expert', 'initiale', 'Atelier pratique pour apprendre les techniques expertes de théâtre d\'objets.', '1 semaine', 35, '09/07/2025 au 16/07/2025', '1 Place Jean-Jaurès, 65000 Tarbes', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans le théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 35, 'valide', NULL),
(36, 'Formation en Marionnettes à Fil Maître', 'continue', 'Formation maître sur les techniques de marionnettes à fil.', '1 mois', 120, '10/07/2025 au 17/07/2025', '8 Cours du Chapeau-Rouge, 33000 Bordeaux', 1200.00, 'Expérience en marionnettes à fil requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 36, 'valide', NULL),
(37, 'Formation Initiale en Théâtre d\'Ombres Maître', 'initiale', 'Introduction aux techniques maître du théâtre d\'ombres.', '2 semaines', 50, '11/07/2025 au 18/07/2025', '7 Cours Gay-Lussac, 87000 Limoges', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 37, 'valide', NULL),
(38, 'Atelier de Marionnettes Contemporaines Maître', 'continue', 'Atelier pratique pour explorer les techniques contemporaines maître de marionnettes.', '3 jours', 21, '12/07/2025 au 19/07/2025', '6 Rue de l’Hôtel-de-Ville, 17000 La Rochelle', 300.00, 'Expérience en marionnettes contemporaines requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 38, 'valide', NULL),
(39, 'Formation en Marionnettes à Gaine Maître', 'initiale', 'Formation complète sur les techniques maître de marionnettes à gaine.', '2 mois', 150, '13/07/2025 au 20/07/2025', '3 Place des Gascons, 64100 Bayonne', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 39, 'valide', NULL),
(40, 'Atelier de Marionnettes Traditionnelles Maître', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles maître de marionnettes.', '1 semaine', 35, '14/07/2025 au 21/07/2025', '48 La Canebière, 13001 Marseille', 400.00, 'Expérience en marionnettes traditionnelles requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 40, 'valide', NULL),
(41, 'Formation Initiale en Arts de la Scène Maître', 'initiale', 'Formation complète sur les arts de la scène maître et les techniques de marionnettes.', '4 mois', 300, '15/07/2025 au 22/07/2025', '37 Promenade des Anglais, 06000 Nice', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 41, 'valide', NULL),
(42, 'Formation Continue en Marionnettes Géantes Maître', 'continue', 'Perfectionnement en création et manipulation maître de marionnettes géantes.', '2 semaines', 70, '16/07/2025 au 23/07/2025', '9 Rue Joseph-Vernet, 84000 Avignon', 800.00, 'Expérience en marionnettes géantes maître requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 42, 'valide', NULL),
(43, 'Atelier de Théâtre d\'Objets Maître', 'initiale', 'Atelier pratique pour apprendre les techniques maître de théâtre d\'objets.', '1 semaine', 35, '17/07/2025 au 24/07/2025', '18 Rue Carnot, 05000 Gap', 400.00, 'Aucun prérequis', 'France Travail', 'Artistes spécialisés dans le théâtre d\'objets.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'Formation Certifiante', 43, 'valide', NULL),
(44, 'Formation en Marionnettes à Fil Grand Maître', 'continue', 'Formation grand maître sur les techniques de marionnettes à fil.', '1 mois', 120, '18/07/2025 au 25/07/2025', '13 Cours Napoléon, 20000 Ajaccio', 1200.00, 'Expérience en marionnettes à fil requise', 'Fondations', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'DE', 44, 'valide', NULL),
(45, 'Formation Initiale en Théâtre d\'Ombres Grand Maître', 'initiale', 'Introduction aux techniques grand maître du théâtre d\'ombres.', '2 semaines', 50, '19/07/2025 au 26/07/2025', '52 Rue de l’Annonciade, 20200 Bastia', 500.00, 'Aucun prérequis', 'Bourses', 'Artistes spécialisés dans le théâtre d\'ombres.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'Formation Certifiante', 45, 'valide', NULL),
(46, 'Atelier de Marionnettes Contemporaines Grand Maître', 'continue', 'Atelier pratique pour explorer les techniques contemporaines grand maître de marionnettes.', '3 jours', 21, '20/07/2025 au 27/07/2025', '115 Rue Frébault, 97110 Pointe-à-Pitre', 300.00, 'Expérience en marionnettes contemporaines requise', 'Employeurs', 'Artistes contemporains.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DNSP', 46, 'valide', NULL),
(47, 'Formation en Marionnettes à Gaine Grand Maître', 'initiale', 'Formation complète sur les techniques grand maître de marionnettes à gaine.', '2 mois', 150, '21/07/2025 au 28/07/2025', '132 Boulevard Pasteur, 97200 Fort-de-France', 1300.00, 'Aucun prérequis', 'Régions', 'Marionnettistes professionnels.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DE', 47, 'valide', NULL),
(48, 'Atelier de Marionnettes Traditionnelles Grand Maître', 'continue', 'Atelier pratique pour apprendre les techniques traditionnelles grand maître de marionnettes.', '1 semaine', 35, '22/07/2025 au 29/07/2025', '31 Boulevard Nelson-Madiba-Mandela, 97300 Cayenne', 400.00, 'Expérience en marionnettes traditionnelles requise', 'Autofinancement', 'Artistes spécialisés dans les marionnettes traditionnelles.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Erasmus+', 'Formation Certifiante', 48, 'valide', NULL),
(49, 'Formation Initiale en Arts de la Scène Grand Maître', 'initiale', 'Formation complète sur les arts de la scène grand maître et les techniques de marionnettes.', '4 mois', 300, '23/07/2025 au 30/07/2025', '60 Rue du Maréchal Leclerc, 97400 Saint-Denis', 2500.00, 'Aucun prérequis', 'OPCO', 'Artistes professionnels des arts de la scène.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Qualiopi', 'DE', 49, 'valide', NULL),
(50, 'Formation Continue en Marionnettes Géantes Grand Maître', 'continue', 'Perfectionnement en création et manipulation grand maître de marionnettes géantes.', '2 semaines', 70, '24/07/2025 au 31/07/2025', '1 Impasse Ylang-Ylang, 97600 Mamoudzou', 800.00, 'Expérience en marionnettes géantes grand maître requise', 'CPF', 'Artistes spécialisés dans les marionnettes géantes.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 'DNSP', 50, 'valide', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Organisme`
--

CREATE TABLE `Organisme` (
  `id_organisme` int NOT NULL,
  `nom` varchar(200) DEFAULT NULL,
  `adresse` varchar(200) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `telephone` varchar(20) NOT NULL,
  `site_web` varchar(100) DEFAULT NULL,
  `presentation` text NOT NULL,
  `num_adherent` varchar(50) DEFAULT NULL,
  `statut` varchar(255) DEFAULT NULL,
  `label` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Organisme`
--

INSERT INTO `Organisme` (`id_organisme`, `nom`, `adresse`, `email`, `telephone`, `site_web`, `presentation`, `num_adherent`, `statut`, `label`) VALUES
(1, 'École Nationale Supérieure des Arts de la Marionnette', '16 avenue Jean Jaurès, 08000 Charleville-Mézières', 'institut@marionnette.com', '0324337250', 'https://marionnette.com', 'L’ESNAM forme des artistes-marionnettistes professionnels dans un cadre d’enseignement supérieur artistique reconnu.', 'A12345', 'Établissement public', 'Qualiopi'),
(2, 'École des Marionnettes de Paris', '10 Avenue des Champs-Élysées, 75008 Paris', 'contact@ecole-marionnettes-paris.com', '0234567890', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École spécialisée dans les arts de la marionnette et du théâtre d\'objets.', 'B67890', 'Entreprise de droit privé', 'RNCP'),
(3, 'Compagnie des Marionnettes de Paris', '3A Rue du 22 Novembre, 67000 Strasbourg', 'contact@compagnie-marionnettes-paris.com', '0345678901', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de théâtre de marionnettes et de spectacles pour enfants.', 'C54321', 'Coopérative', 'Erasmus+'),
(4, 'Atelier des Marionnettes de Paris', '103 Rue de Vesle, 51100 Reims', 'contact@atelier-marionnettes-paris.com', '0456789012', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux marionnettes.', 'D98765', 'Etablissement public', 'Qualiopi'),
(5, 'Centre des Marionnettes de Paris', '10 Rue Saint-Dizier, 54000 Nancy', 'contact@centre-marionnettes-paris.com', '0567890123', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'E43210', 'Collectivité', 'RNCP'),
(6, 'Théâtre des Marionnettes de Lille', '7 Boulevard de l’Europe, 68100 Mulhouse', 'contact@theatre-marionnettes-lille.com', '0678901234', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'F12345', 'Association loi 1901', 'Erasmus+'),
(7, 'École des Marionnettes de Arras', '8 Place de la République, 59000 Lille', 'contact@ecole-marionnettes-arras.com', '0789012345', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'G67890', 'Entreprise de droit privé', 'Qualiopi'),
(8, 'Compagnie des Marionnettes de Amiens', '7 Rue des Vergeaux, 80000 Amiens', 'contact@compagnie-marionnettes-amiens.com', '0890123456', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'H54321', 'Coopérative', 'RNCP'),
(9, 'Atelier des Marionnettes de Calais', '18 Rue des Fontinettes, 62100 Calais', 'contact@atelier-marionnettes-calais.com', '0901234567', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'I98765', 'Etablissement public', 'Erasmus+'),
(10, 'Institut des Marionnettes de Compiègne', '1 Rue de Lyon, 02100 Saint-Quentin', 'contact@institut-marionnettes-compiegne.com', '0101234568', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Institut de formation aux arts de la marionnette et du théâtre.', 'J43210', 'Collectivité', 'Qualiopi'),
(11, 'École des Marionnettes de Deauville', '45 bis Rue Jeanne-d’Arc, 76000 Rouen', 'contact@ecole-marionnettes-deauville.com', '0111234569', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École spécialisée dans les arts de la marionnette.', 'K12345', 'Association loi 1901', 'RNCP'),
(12, 'Compagnie des Marionnettes de Rouen', '5 Rue des Boutiques, 14000 Caen', 'contact@compagnie-marionnettes-rouen.com', '0121234560', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de théâtre de marionnettes et de spectacles pour enfants.', 'L67890', 'Entreprise de droit privé', 'Erasmus+'),
(13, 'Atelier des Marionnettes de Caen', '172 Boulevard de Strasbourg, 76600 Le Havre', 'contact@atelier-marionnettes-caen.com', '0131234561', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux marionnettes.', 'M54321', 'Coopérative', 'Qualiopi'),
(14, 'Centre des Marionnettes de Saint-Lô', '1 Rue de l’Ancien-Quai, 50100 Cherbourg-en-Cotentin', 'contact@centre-marionnettes-saintlo.com', '0141234562', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'N98765', 'Etablissement public', 'RNCP'),
(15, 'Théâtre des Marionnettes de Granville', '11 Place Sainte-Anne, 35000 Rennes', 'contact@theatre-marionnettes-granville.com', '0151234563', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'O43210', 'Collectivité', 'Erasmus+'),
(16, 'École des Marionnettes de Rennes', '25 Place de la République, 56000 Vannes', 'contact@ecole-marionnettes-rennes.com', '0161234564', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'P12345', 'Association loi 1901', 'Qualiopi'),
(17, 'Compagnie des Marionnettes de Brest', '5 Place de la Résistance, 22000 Saint-Brieuc', 'contact@compagnie-marionnettes-brest.com', '0171234565', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'Q67890', 'Entreprise de droit privé', 'RNCP'),
(18, 'Atelier des Marionnettes de Lorient', '17 Allée des Tanneurs, 44000 Nantes', 'contact@atelier-marionnettes-lorient.com', '0181234566', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'R54321', 'Coopérative', 'Erasmus+'),
(19, 'Institut des Marionnettes de Saint-Brieuc', '1 Rue Franklin-Roosevelt, 49100 Angers', 'contact@institut-marionnettes-saintbrieuc.com', '0191234567', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Institut de formation aux arts de la marionnette et du théâtre.', 'S98765', 'Etablissement public', 'Qualiopi'),
(20, 'École des Marionnettes de Quimper', '13 Place de la République, 72000 Le Mans', 'contact@ecole-marionnettes-quimper.com', '0201234568', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École spécialisée dans les arts de la marionnette.', 'T43210', 'Collectivité', 'RNCP'),
(21, 'Compagnie des Marionnettes de Nantes', '8 Rue Georges Clemenceau, 85000 La Roche-sur-Yon', 'contact@compagnie-marionnettes-nantes.com', '0211234569', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de théâtre de marionnettes et de spectacles pour enfants.', 'U12345', 'Association loi 1901', 'Erasmus+'),
(22, 'Atelier des Marionnettes de La Roche-sur-Yon', '10 Place du Châtelet, 45000 Orléans', 'contact@atelier-marionnettes-larochesuryon.com', '0221234560', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux marionnettes.', 'V67890', 'Entreprise de droit privé', 'Qualiopi'),
(23, 'Centre des Marionnettes de Le Mans', '1 Boulevard Béranger, 37000 Tours', 'contact@centre-marionnettes-lemans.com', '0231234561', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'W54321', 'Coopérative', 'RNCP'),
(24, 'Théâtre des Marionnettes de Angers', '29 Rue Moyenne, 18000 Bourges', 'contact@theatre-marionnettes-angers.com', '0241234562', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'X98765', 'Etablissement public', 'Erasmus+'),
(25, 'École des Marionnettes de Laval', '26 Boulevard Georges Clemenceau, 21000 Dijon', 'contact@ecole-marionnettes-laval.com', '0251234563', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'Y43210', 'Collectivité', 'Qualiopi'),
(26, 'Compagnie des Marionnettes de Bordeaux', '44 Rue de Belfort, 25000 Besançon', 'contact@compagnie-marionnettes-bordeaux.com', '0261234564', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'Z12345', 'Association loi 1901', 'RNCP'),
(27, 'Atelier des Marionnettes de Bayonne', '25 bis Avenue Pierre-Bérégovoy, 58000 Nevers', 'contact@atelier-marionnettes-bayonne.com', '0271234565', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'A67890', 'Entreprise de droit privé', 'Erasmus+'),
(28, 'Institut des Marionnettes de Limoges', '24 Rue de la République, 69002 Lyon', 'contact@institut-marionnettes-limoges.com', '0281234566', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Institut de formation aux arts de la marionnette et du théâtre.', 'B54321', 'Coopérative', 'Qualiopi'),
(29, 'École des Marionnettes de Poitiers', '12 Avenue Alsace-Lorraine, 38000 Grenoble', 'contact@ecole-marionnettes-poitiers.com', '0291234567', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École spécialisée dans les arts de la marionnette.', 'C98765', 'Etablissement public', 'RNCP'),
(30, 'Compagnie des Marionnettes de Périgueux', '22 Place de Jaude, 63000 Clermont-Ferrand', 'contact@compagnie-marionnettes-perigueux.com', '0301234568', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de théâtre de marionnettes et de spectacles pour enfants.', 'D43210', 'Association loi 1901', 'Erasmus+'),
(31, 'Atelier des Marionnettes de Toulouse', '1 Rue de la Poste, 74000 Annecy', 'contact@atelier-marionnettes-toulouse.com', '0311234569', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux marionnettes.', 'E12345', 'Entreprise de droit privé', 'Qualiopi'),
(32, 'Centre des Marionnettes de Montpellier', '9 Rue Lafayette, 31000 Toulouse', 'contact@centre-marionnettes-montpellier.com', '0321234560', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'F67890', 'Coopérative', 'RNCP'),
(33, 'Théâtre des Marionnettes de Perpignan', '33 Rue de la Cavalerie, 34000 Montpellier', 'contact@theatre-marionnettes-perpignan.com', '0331234561', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'G54321', 'Etablissement public', 'Erasmus+'),
(34, 'École des Marionnettes de Toulouse', '19 Boulevard Georges Clemenceau, 66000 Perpignan', 'contact@ecole-marionnettes-toulouse.com', '0341234562', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'H98765', 'Collectivité', 'Qualiopi'),
(35, 'Compagnie des Marionnettes de Nîmes', '1 Place Jean-Jaurès, 65000 Tarbes', 'contact@compagnie-marionnettes-nimes.com', '0351234563', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'I43210', 'Association loi 1901', 'RNCP'),
(36, 'Atelier des Marionnettes de Nice', '8 Cours du Chapeau-Rouge, 33000 Bordeaux', 'contact@atelier-marionnettes-nice.com', '0361234564', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'J12345', 'Entreprise de droit privé', 'Erasmus+'),
(37, 'Centre des Marionnettes de Marseille', '7 Cours Gay-Lussac, 87000 Limoges', 'contact@centre-marionnettes-marseille.com', '0371234565', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'K67890', 'Coopérative', 'Qualiopi'),
(38, 'Théâtre des Marionnettes de Aix-en-Provence', '6 Rue de l’Hôtel-de-Ville, 17000 La Rochelle', 'contact@theatre-marionnettes-aixenprovence.com', '0381234566', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'L54321', 'Etablissement public', 'RNCP'),
(39, 'École des Marionnettes de Nice', '3 Place des Gascons, 64100 Bayonne', 'contact@ecole-marionnettes-nice.com', '0391234567', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'M98765', 'Collectivité', 'Qualiopi'),
(40, 'Compagnie des Marionnettes de Avignon', '48 La Canebière, 13001 Marseille', 'contact@compagnie-marionnettes-avignon.com', '0401234568', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'N43210', 'Association loi 1901', 'RNCP'),
(41, 'Atelier des Marionnettes de Lyon', '37 Promenade des Anglais, 06000 Nice', 'contact@atelier-marionnettes-lyon.com', '0411234569', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'O12345', 'Entreprise de droit privé', 'Erasmus+'),
(42, 'Institut des Marionnettes de Lyon', '9 Rue Joseph-Vernet, 84000 Avignon', 'contact@institut-marionnettes-lyon.com', '0421234560', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Institut de formation aux arts de la marionnette et du théâtre.', 'P67890', 'Coopérative', 'Qualiopi'),
(43, 'École des Marionnettes de Clermont-Ferrand', '18 Rue Carnot, 05000 Gap', 'contact@ecole-marionnettes-clermontferrand.com', '0431234561', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École spécialisée dans les arts de la marionnette.', 'Q54321', 'Etablissement public', 'RNCP'),
(44, 'Compagnie des Marionnettes de Grenoble', '13 Cours Napoléon, 20000 Ajaccio', 'contact@compagnie-marionnettes-grenoble.com', '0441234562', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de théâtre de marionnettes et de spectacles pour enfants.', 'R98765', 'Association loi 1901', 'Erasmus+'),
(45, 'Atelier des Marionnettes de Annecy', '52 Rue de l’Annonciade, 20200 Bastia', 'contact@atelier-marionnettes-annecy.com', '0451234563', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'S43210', 'Entreprise de droit privé', 'Qualiopi'),
(46, 'Centre des Marionnettes de Strasbourg', '115 Rue Frébault, 97110 Pointe-à-Pitre', 'contact@centre-marionnettes-strasbourg.com', '0461234564', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Centre de formation et de création de marionnettes.', 'T12345', 'Coopérative', 'RNCP'),
(47, 'Théâtre des Marionnettes de Reims', '132 Boulevard Pasteur, 97200 Fort-de-France', 'contact@theatre-marionnettes-reims.com', '0471234565', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Théâtre spécialisé dans les spectacles de marionnettes.', 'U67890', 'Etablissement public', 'Erasmus+'),
(48, 'École des Marionnettes de Metz', '31 Boulevard Nelson-Madiba-Mandela, 97300 Cayenne', 'contact@ecole-marionnettes-metz.com', '0481234566', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'École de formation aux techniques de marionnettes.', 'V54321', 'Collectivité', 'Qualiopi'),
(49, 'Compagnie des Marionnettes de Épinal', '60 Rue du Maréchal Leclerc, 97400 Saint-Denis', 'contact@compagnie-marionnettes-epinal.com', '0491234567', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Compagnie de marionnettes et de théâtre d\'objets.', 'W98765', 'Association loi 1901', 'RNCP'),
(50, 'Atelier des Marionnettes de Nancy', '1 Impasse Ylang-Ylang, 97600 Mamoudzou', 'contact@atelier-marionnettes-nancy.com', '0501234568', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'Atelier de création et de formation aux arts de la marionnette.', 'X43210', 'Entreprise de droit privé', 'Erasmus+');

-- --------------------------------------------------------

--
-- Structure de la table `Utilisateur`
--

CREATE TABLE `Utilisateur` (
  `id_utilisateur` int NOT NULL,
  `nom` varchar(150) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('visiteur','user','admin') NOT NULL DEFAULT 'visiteur',
  `num_adherent` varchar(150) DEFAULT NULL,
  `id_organisme` int DEFAULT NULL,
  `photo_profil` varchar(255) DEFAULT NULL,
  `reset_token` varchar(100) DEFAULT NULL,
  `reset_token_expiration` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Utilisateur`
--

INSERT INTO `Utilisateur` (`id_utilisateur`, `nom`, `email`, `mot_de_passe`, `role`, `num_adherent`, `id_organisme`, `photo_profil`, `reset_token`, `reset_token_expiration`) VALUES
(1, 'Admin THEMAA', 'admin@admin.com', '$2b$12$SOMEHASHEDPASSWORD1', 'admin', NULL, NULL, NULL, NULL, NULL),
(2, 'Jean Dupont', 'jean@exemple.com', '$2b$12$SOMEHASHEDPASSWORD2', 'user', NULL, NULL, NULL, NULL, NULL),
(3, 'Utilisateur THEMAA', 'user@themaa.fr', '$2b$12$SOMEHASHEDPASSWORD3', 'user', NULL, NULL, NULL, NULL, NULL),
(4, 'Compagnie des Songes', 'contact@cie-songes.fr', '$2b$12$SOMEHASHEDPASSWORD4', 'user', NULL, NULL, NULL, NULL, NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Formation`
--
ALTER TABLE `Formation`
  ADD PRIMARY KEY (`id_formation`),
  ADD KEY `id_organisme` (`id_organisme`);

--
-- Index pour la table `Organisme`
--
ALTER TABLE `Organisme`
  ADD PRIMARY KEY (`id_organisme`);

--
-- Index pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  ADD PRIMARY KEY (`id_utilisateur`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `id_organisme` (`id_organisme`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Formation`
--
ALTER TABLE `Formation`
  MODIFY `id_formation` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT pour la table `Organisme`
--
ALTER TABLE `Organisme`
  MODIFY `id_organisme` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  MODIFY `id_utilisateur` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Formation`
--
ALTER TABLE `Formation`
  ADD CONSTRAINT `Formation_ibfk_1` FOREIGN KEY (`id_organisme`) REFERENCES `Organisme` (`id_organisme`);

--
-- Contraintes pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  ADD CONSTRAINT `Utilisateur_ibfk_1` FOREIGN KEY (`id_organisme`) REFERENCES `Organisme` (`id_organisme`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
