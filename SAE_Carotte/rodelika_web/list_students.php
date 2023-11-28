<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: login.html");
    exit();
}

// Configuration de la base de données
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "purpledragon";

// Connexion à la base de données
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

// Requête SQL pour récupérer la liste des étudiants
$sql = "SELECT etu_id, etu_nom, etu_prenom FROM etudiant";
$result = $conn->query($sql);

// Vérifier si la requête a réussi
if ($result === false) {
    die("Erreur lors de l'exécution de la requête : " . $conn->error);
}

// Afficher les étudiants
echo "<h1>Liste des étudiants</h1>";

if ($result->num_rows > 0) {
    echo "<ul>";
    while ($row = $result->fetch_assoc()) {
        echo "<li>ID: " . $row["etu_id"] . ", Nom: " . $row["etu_nom"] . ", Prénom: " . $row["etu_prenom"] . "</li>";
    }
    echo "</ul>";
} else {
    echo "Aucun étudiant trouvé.";
}

// Fermer la connexion à la base de données
$conn->close();
?>
