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

// Requête SQL pour récupérer les soldes des étudiants
$sql = "SELECT etudiant.etu_id, etudiant.etu_nom, etudiant.etu_prenom, IFNULL(SUM(compte.opr_montant), 0) as total FROM etudiant LEFT JOIN compte ON etudiant.etu_id = compte.etu_id GROUP BY etudiant.etu_id";
$result = $conn->query($sql);

// Vérifier si la requête a réussi
if ($result === false) {
    die("Erreur lors de l'exécution de la requête : " . $conn->error);
}

// Afficher les soldes des étudiants
echo "<h1>Solde des étudiants</h1>";

if ($result->num_rows > 0) {
    echo "<ul>";
    while ($row = $result->fetch_assoc()) {
        echo "<li>" . $row["etu_nom"] . " " . $row["etu_prenom"] . " : " . $row["total"] . "€</li>";
    }
    echo "</ul>";
} else {
    echo "Aucun étudiant trouvé.";
}

// Fermer la connexion à la base de données
$conn->close();
?>
