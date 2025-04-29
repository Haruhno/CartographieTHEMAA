-- Création de la table Organisme
CREATE TABLE Organisme (
    id_organisme INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    adresse VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    site_web VARCHAR(100) DEFAULT NULL,
    presentation TEXT NOT NULL,
    num_adherent VARCHAR(50) DEFAULT NULL,
    statut VARCHAR(50) NOT NULL,
    label VARCHAR(50) DEFAULT NULL
);

-- Données de test pour Organisme
INSERT INTO Organisme (nom, adresse, email, telephone, site_web, presentation, num_adherent, statut, label) VALUES
('École Nationale des Arts de la Marionnette', '7 Rue Saint-Jacques, 75005 Paris', 'contact@enam-marionnette.fr', '0143259876', 'www.enam-marionnette.fr', 'École de référence dans la formation aux arts de la marionnette depuis 1987.', 'ENAM123', 'Association loi 1901', 'Qualiopi'),
('Compagnie des Petits Pas', '12 Rue du Théâtre, 31000 Toulouse', 'cie.petitspas@example.com', '0561123456', 'www.ciepetitspas.fr', 'Compagnie professionnelle proposant des formations continues.', 'CPP456', 'SARL', NULL),
('Atelier Marionnette et Thérapie', '5 Boulevard des Arts, 69002 Lyon', 'marionnette.therapie@example.com', '0478563412', NULL, 'Association spécialisée dans l''utilisation thérapeutique de la marionnette.', 'AMT789', 'Association', NULL);

-- Création de la table Formation
CREATE TABLE Formation (
    id_formation INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    type ENUM('initiale', 'continue') NOT NULL,
    description TEXT NOT NULL,
    duree VARCHAR(50) NOT NULL,
    dates VARCHAR(100) NOT NULL,
    lieu VARCHAR(100) NOT NULL,
    prix DECIMAL(10,2) DEFAULT NULL,
    conditions_acces TEXT DEFAULT NULL,
    financement VARCHAR(100) DEFAULT NULL,
    presentation_intervenants TEXT DEFAULT NULL,
    lien_inscription VARCHAR(200) DEFAULT NULL,
    label VARCHAR(50) DEFAULT NULL,
    id_organisme INT NOT NULL,
    FOREIGN KEY (id_organisme) REFERENCES Organisme(id_organisme) ON DELETE CASCADE
);

-- Données de test pour Formation
INSERT INTO Formation (nom, type, description, duree, dates, lieu, prix, conditions_acces, financement, presentation_intervenants, lien_inscription, label, id_organisme) VALUES
('Diplôme d''Artiste Marionnettiste', 'initiale', 'Formation complète de 3 ans aux techniques de manipulation, construction et mise en scène.', '3 ans', 'Septembre 2024 - Juin 2027', 'Paris', 4500.00, 'Baccalauréat ou équivalent, entretien et audition', 'Bourse possible', 'Intervenants professionnels du spectacle vivant', 'www.enam-marionnette.fr/inscription', 'RNCP', 1),
('Stage de Marionnette Thérapeutique', 'continue', 'Formation de 5 jours sur l''utilisation de la marionnette en contexte thérapeutique.', '5 jours', '15-19 novembre 2024', 'Lyon', 650.00, 'Expérience dans le soin ou l''éducation', 'CPF, OPCO', 'Psychologues et art-thérapeutes spécialisés', 'www.marionnette-therapie.com/stages', NULL, 3),
('Atelier Construction de Marionnettes', 'continue', 'Week-end d''initiation à la fabrication de marionnettes en matériaux recyclés.', '2 jours', '12-13 octobre 2024', 'Toulouse', 120.00, 'Aucun prérequis', 'Financement personnel', 'Artisans marionnettistes de la compagnie', 'www.ciepetitspas.fr/ateliers', NULL, 2);

-- Création de la table Utilisateur (version anglaise des rôles)
CREATE TABLE Utilisateur (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('visitor', 'user', 'admin') NOT NULL,
    num_adherent VARCHAR(50) DEFAULT NULL
);

-- Données de test avec rôles en anglais
INSERT INTO Utilisateur (nom, email, mot_de_passe, role, num_adherent) VALUES
('Admin THEMAA', 'admin@themaa.org', '$2y$10$N9qo8uLOickgx2ZMRZoMy.MH/rW8QJRTiF8tS7X2QjkL7GYbYFdG2', 'admin', NULL),
('Compagnie des Songes', 'contact@cie-songes.fr', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'user', 'CSG321'),
('Jean Dupont', 'jean.dupont@example.com', '$2y$10$TKh8H1.PfQx37YgCzwiKb.KjNyWgaHb9cbcoQgdIVFlYg7B77UdFm', 'visitor', NULL);

