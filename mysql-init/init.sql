-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : mer. 28 mai 2025 à 15:47
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
-- Base de données : `themapp_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `Formation`
--

CREATE TABLE `Formation` (
  `id_formation` int NOT NULL,
  `nom` varchar(100) NOT NULL,
  `type` enum('initiale','continue') NOT NULL,
  `description` text NOT NULL,
  `duree` varchar(50) NOT NULL,
  `dates` varchar(100) NOT NULL,
  `lieu` varchar(100) NOT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `conditions_acces` text,
  `financement` varchar(100) DEFAULT NULL,
  `presentation_intervenants` text,
  `lien_inscription` varchar(200) DEFAULT NULL,
  `label` varchar(50) DEFAULT NULL,
  `id_organisme` int NOT NULL,
  `etat` enum('valide','en_attente') NOT NULL DEFAULT 'en_attente',
  `raison` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Formation`
--

INSERT INTO `Formation` (`id_formation`, `nom`, `type`, `description`, `duree`, `dates`, `lieu`, `prix`, `conditions_acces`, `financement`, `presentation_intervenants`, `lien_inscription`, `label`, `id_organisme`, `etat`, `raison`) VALUES
(1, 'Diplôme National d\'Arts de la Marionnette', 'initiale', 'Formation complète en arts de la marionnette à l\'ESNAM, comprenant théorie et pratique.', '3 ans', 'Septembre 2025 - Juin 2028', 'Charleville-Mézières', 0.00, 'Baccalauréat ou équivalent requis', 'Bourses, aides régionales', 'Intervenants professionnels et artistes reconnus.', 'https://marionnette.com/esnam-formations/esnam/ecole/', 'RNCP', 1, 'valide', NULL),
(2, 'Atelier de Fabrication de Marionnettes', 'continue', 'Stage pratique de création de marionnettes artisanales.', '2 jours', '10-11 juin 2025', 'Paris', 200.00, 'Aucun prérequis', 'Financement personnel', 'Artisans spécialisés et artistes plasticiens.', 'https://www.ateliermarionnettesparis.fr/stages', 'Qualiopi', 2, 'valide', NULL),
(3, 'Formation Continue en Théâtre de Marionnettes', 'continue', 'Cours intensifs sur les techniques avancées du théâtre de marionnettes.', '10 jours', '15-25 juillet 2025', 'Lyon', 850.00, 'Expérience théâtrale recommandée', 'CPF, OPCO', 'Professionnels du spectacle et pédagogues.', 'https://www.institutmarionnetteslyon.fr/formations', NULL, 3, 'valide', NULL),
(4, 'Stage d\'Initiation aux Marionnettes pour Enfants', 'initiale', 'Atelier ludique pour enfants, découverte des marionnettes.', '1 jour', '12 août 2025', 'Marseille', 50.00, 'Aucun', 'Financement personnel', 'Animateurs et artistes.', 'https://www.compagnie-mediterranee.fr/ateliers', 'Qualiopi', 4, 'valide', NULL),
(5, 'Cycle Professionnel en Arts de la Marionnette', 'initiale', 'Programme complet de formation professionnelle.', '2 ans', 'Octobre 2025 - Juin 2027', 'Bordeaux', 0.00, 'Baccalauréat artistique ou équivalent', 'Subventions, aides à la formation', 'Intervenants professionnels du secteur.', 'https://www.ecolemarionnettesbordeaux.fr/inscriptions', 'RNCP', 5, 'valide', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Organisme`
--

CREATE TABLE `Organisme` (
  `id_organisme` int NOT NULL,
  `nom` varchar(100) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `site_web` varchar(100) DEFAULT NULL,
  `presentation` text NOT NULL,
  `num_adherent` varchar(50) DEFAULT NULL,
  `statut` varchar(50) NOT NULL,
  `label` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Organisme`
--

INSERT INTO `Organisme` (`id_organisme`, `nom`, `adresse`, `email`, `telephone`, `site_web`, `presentation`, `num_adherent`, `statut`, `label`) VALUES
(1, 'École Nationale Supérieure des Arts de la Marionnette', '16 Av. Jean Jaurès, 08000 Charleville-Mézières', 'contact@esnam.fr', '0324356789', 'https://www.esnam.fr', 'École nationale d\'arts spécialisée en formation aux arts de la marionnette.', NULL, 'Établissement public', 'RNCP'),
(2, 'Atelier Marionnettes de Paris', '12 Rue des Arts, 75003 Paris', 'contact@ateliermarionnettesparis.fr', '0145789632', 'https://www.ateliermarionnettesparis.fr', 'Atelier de création et formation en marionnettes pour amateurs et professionnels.', NULL, 'Association loi 1901', 'Qualiopi'),
(3, 'Institut des Marionnettes de Lyon', '45 Rue des Marionnettes, 69007 Lyon', 'contact@institutmarionnetteslyon.fr', '0472389456', 'https://www.institutmarionnetteslyon.fr', 'Institut de formation et recherche dans le domaine des arts de la marionnette.', NULL, 'SARL', NULL),
(4, 'Compagnie Marionnettes Méditerranée', '78 Avenue du Théâtre, 13006 Marseille', 'contact@compagnie-mediterranee.fr', '0491234567', 'https://www.compagnie-mediterranee.fr', 'Compagnie de théâtre de marionnettes et spectacles itinérants.', NULL, 'Association loi 1901', 'Qualiopi'),
(5, 'École des Arts de la Marionnette - Bordeaux', '10 Quai des Chartrons, 33000 Bordeaux', 'contact@ecolemarionnettesbordeaux.fr', '0556789123', 'https://www.ecolemarionnettesbordeaux.fr', 'Formation initiale et continue en arts de la marionnette.', NULL, 'Établissement privé', 'RNCP');

-- --------------------------------------------------------

--
-- Structure de la table `Utilisateur`
--

CREATE TABLE `Utilisateur` (
  `id_utilisateur` int NOT NULL,
  `nom` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('user','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `num_adherent` varchar(50) DEFAULT NULL,
  `id_organisme` int DEFAULT NULL,
  `photo_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `Utilisateur`
--

INSERT INTO `Utilisateur` (`id_utilisateur`, `nom`, `email`, `mot_de_passe`, `role`, `num_adherent`, `id_organisme`, `photo_profil`) VALUES
(1, 'Admin THEMAA', 'admin@themaa.org', '$2y$10$N9qo8uLOickgx2ZMRZoMy.MH/rW8QJRTiF8tS7X2QjkL7GYbYFdG2', 'admin', NULL, NULL, NULL),
(2, 'Compagnie des Songes', 'contact@cie-songes.fr', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'user', 'CSG321', NULL, NULL),
(3, 'Jean Dupont', 'jean.dupont@example.com', '$2y$10$TKh8H1.PfQx37YgCzwiKb.KjNyWgaHb9cbcoQgdIVFlYg7B77UdFm', 'user', NULL, NULL, NULL),
(4, 'admin', 'admin@admin.com', 'scrypt:32768:8:1$qvs7RJ3GE8hIaLYp$046077051766a217c28f30f6ab6323b425f58ccdee7748a91c01a8e022f5b10a0db5d083897e873e2a95b5cd81cfe99ba516b68de898972ef7ac92f82a8dafd7', 'admin', NULL, NULL, NULL),
(5, 'Utilisateur THEMAA', 'user@themaa.fr', 'scrypt:32768:8:1$4xcTEMvakfxxwyCx$10d81cddb9904373a83994edf72392fa1e57c12aa6310b1417f06ed48447338a7a56a413ff8a7fb4b1e8c8af25fc0a42658a27f6c5d5111d48fd3aadb61f5cda', 'user', 'ABC1234', NULL, NULL),
(6, 'Jane Doe', 'jane.doe@gmail.com', 'scrypt:32768:8:1$fQQ16E7TAr60vTWH$b39f818e85dc1e46db1509671641dd10f221e3a72c8d7ec11ff6b0a79ff8fe4eec0e0d7497d42dabe63ab8792579fd3512a044a793a06ddcc15b546c8e2ff27f', 'user', NULL, 1, NULL);

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
  ADD KEY `fk_utilisateur_organisme` (`id_organisme`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Formation`
--
ALTER TABLE `Formation`
  MODIFY `id_formation` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `Organisme`
--
ALTER TABLE `Organisme`
  MODIFY `id_organisme` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  MODIFY `id_utilisateur` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Formation`
--
ALTER TABLE `Formation`
  ADD CONSTRAINT `Formation_ibfk_1` FOREIGN KEY (`id_organisme`) REFERENCES `Organisme` (`id_organisme`) ON DELETE CASCADE;

--
-- Contraintes pour la table `Utilisateur`
--
ALTER TABLE `Utilisateur`
  ADD CONSTRAINT `fk_utilisateur_organisme` FOREIGN KEY (`id_organisme`) REFERENCES `Organisme` (`id_organisme`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
