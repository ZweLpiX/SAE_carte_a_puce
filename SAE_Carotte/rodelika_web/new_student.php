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

// Vérification si le formulaire a été soumis
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Connexion à la base de données
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Vérifier la connexion
    if ($conn->connect_error) {
        die("La connexion à la base de données a échoué : " . $conn->connect_error);
    }

    // Récupérer et valider les données du formulaire
    $nom = isset($_POST["nom"]) ? trim(mysqli_real_escape_string($conn, $_POST["nom"])) : null;
    $prenom = isset($_POST["prenom"]) ? trim(mysqli_real_escape_string($conn, $_POST["prenom"])) : null;

    // Vérifier si les champs ne sont pas vides
    if (empty($nom) || empty($prenom)) {
        $response = array(
            'success' => false,
            'message' => 'Tous les champs doivent être remplis.'
        );
    } else {
        // Requête SQL préparée pour insérer un nouvel étudiant
        $sql = $conn->prepare("INSERT INTO etudiant (etu_nom, etu_prenom) VALUES (?, ?)");
        $sql->bind_param("ss", $nom, $prenom);

        $response = array();

        if ($sql->execute()) {
            $response['success'] = true;
            $response['message'] = "Étudiant ajouté avec succès : $nom $prenom";
        } else {
            $response['success'] = false;
            $response['message'] = "Erreur lors de l'ajout de l'étudiant : " . $sql->error;
        }

        // Fermer la connexion à la base de données
        $sql->close();
    }

    // Fermer la connexion à la base de données
    $conn->close();

    echo json_encode($response);
}
?>
