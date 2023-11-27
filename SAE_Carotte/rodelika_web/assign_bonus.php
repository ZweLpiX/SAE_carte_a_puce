<?php

session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: login.html");
    exit();
}

include 'config.php';

$conn = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);


if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

$etu_id = isset($_POST['etu_id']) ? trim(mysqli_real_escape_string($conn, $_POST['etu_id'])) : null;
$montant = isset($_POST['montant']) ? trim(mysqli_real_escape_string($conn, $_POST['montant'])) : null;
$commentaire = isset($_POST['commentaire']) ? trim(mysqli_real_escape_string($conn, $_POST['commentaire'])) : null;

$response = array();

// Vérifier si les champs ne sont pas vides
if (empty($etu_id) || empty($montant) || empty($commentaire)) {
    $response = array(
        'success' => false,
        'message' => 'Tous les champs doivent être remplis.'
    );
} else {
    // Insérer le bonus dans la base de données
    $sql = $conn->prepare("INSERT INTO compte (etu_id, opr_date, opr_montant, opr_libelle, type_operation) VALUES (?, NOW(), ?, ?, 'Bonus')");
    $sql->bind_param("isd", $etu_id, $montant, $commentaire);

    if ($sql->execute()) {
        $response['success'] = true;
        $response['message'] = "Bonus attribué avec succès à l'étudiant (ID: $etu_id)";
    } else {
        $response['success'] = false;
        $response['message'] = "Erreur lors de l'attribution du bonus : " . $sql->error;
    }

    $sql->close();
}

$conn->close();

echo json_encode($response);
?>
