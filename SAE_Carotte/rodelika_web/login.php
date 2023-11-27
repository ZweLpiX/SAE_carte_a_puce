<?php
session_start();

include 'config.php';

$conn = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);

    // Utilisation de password_hash pour générer le hachage Bcrypt du mot de passe
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    $sql = $conn->prepare("SELECT id, motdepasse FROM utilisateurs WHERE utilisateur = ?");
    $sql->bind_param("s", $username);
    $sql->execute();
    $sql->store_result();

    if ($sql->num_rows > 0) {
        // L'utilisateur existe, récupère le mot de passe haché
        $sql->bind_result($userId, $storedPassword);
        $sql->fetch();

        // Utilise password_verify pour comparer le mot de passe fourni avec le hachage stocké
        if (password_verify($password, $storedPassword)) {
            $_SESSION['user_id'] = $userId;
            header("Location: index.html");
            exit();
        } else {
            $error = "Nom d'utilisateur ou mot de passe incorrect.";
        }
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
</body>
</html>
