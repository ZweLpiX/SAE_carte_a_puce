// login.js
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        // Envoyer les informations de connexion au serveur
        var formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        var responsePromise = fetch('login.php', {
            method: 'POST',
            body: formData
        });

        responsePromise
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Rediriger vers la page principale après la connexion réussie
                    window.location.href = 'index.html';
                } else {
                    alert('Échec de la connexion. Vérifiez vos informations d\'identification.');
                }
            })
            .catch(error => console.error('Erreur lors de la connexion:', error));
    });
});
