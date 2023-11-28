<?php
session_start();

$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "purpledragon";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);

    $sql = $conn->prepare("SELECT id, motdepasse FROM utilisateurs WHERE utilisateur = ?");
    $sql->bind_param("s", $username);
    $sql->execute();
    $sql->store_result();
    $sql->bind_result($id, $storedPassword);

    if ($sql->num_rows > 0 && $sql->fetch() && $password === $storedPassword) {
        $_SESSION['user_id'] = $id;
        header("Location: index.html"); // Redirection vers la page principale
        exit();
    } else {
        $error = "Nom d'utilisateur ou mot de passe incorrect.";
    }

    $sql->close();
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion</title>
</head>
<body>
    <h1>Connexion</h1>
    <?php if (isset($error)) { echo "<p>$error</p>"; } ?>
    <!-- Ajoutez ici le formulaire de connexion si vous souhaitez qu'il reste sur la même page en cas d'erreur -->
</body>
</html>
