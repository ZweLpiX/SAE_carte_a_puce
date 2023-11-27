// main.js
document.addEventListener('DOMContentLoaded', function () {
    // Attacher les événements aux boutons après le chargement du DOM
    document.getElementById('listStudentsBtn').addEventListener('click', listStudents);
    document.getElementById('studentBalancesBtn').addEventListener('click', studentBalances);
    document.getElementById('newStudentFormBtn').addEventListener('click', newstudents);
    document.getElementById('assignBonusFormBtn').addEventListener('click', assignBonusForm);
    document.getElementById('showCreditsBtn').addEventListener('click', showCredits);

    // Ajouter l'événement au formulaire de connexion
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

// Fonction pour charger le contenu depuis le serveur
function loadContent(page, callback) {
    var contentDiv = document.getElementById('content');

    fetch(page)
        .then(response => response.text())
        .then(data => {
            contentDiv.innerHTML = data;
            if (callback) {
                callback(); // Appeler la fonction de rappel s'il y en a une
            }
        })
        .catch(error => console.error('Erreur lors du chargement de la page:', error));
}

// Fonction pour afficher la liste des étudiants
function listStudents() {
    loadContent('list_students.php');
}

// Fonction pour afficher les soldes des étudiants
function studentBalances() {
    loadContent('student_balances.php');
}

// Fonction pour ajouter un nouvel étudiant
function newstudents() {
    var nom = prompt("Entrez le nom de l'étudiant:");
    var prenom = prompt("Entrez le prénom de l'étudiant:");

    var formData = new FormData();
    formData.append('nom', nom);
    formData.append('prenom', prenom);

    var responsePromise = fetch('new_student.php', {
        method: 'POST',
        body: formData
    });

    responsePromise
        .then(response => response.json())
        .then(data => {
            var decodedMessage = decodeURIComponent(data.message);
            alert(decodedMessage);

            if (data.success) {
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error('Erreur lors de la création de l\'étudiant:', error));
}

// Fonction pour attribuer un bonus à un étudiant
function assignBonusForm() {
    var etu_id = prompt("Entrez l'ID de l'étudiant:");
    var montant = prompt("Entrez le montant du bonus:");
    var commentaire = prompt("Entrez un commentaire:");

    var formData = new FormData();
    formData.append('etu_id', etu_id);
    formData.append('montant', montant);
    formData.append('commentaire', commentaire);

    var responsePromise = fetch('assign_bonus.php', {
        method: 'POST',
        body: formData
    });

    responsePromise
        .then(response => response.json())
        .then(data => {
            var decodedMessage = decodeURIComponent(data.message);
            alert(decodedMessage);

            if (data.success) {
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error('Erreur lors de l\'attribution du bonus:', error));
}

// Fonction pour afficher la page des crédits
function showCredits() {
    loadContent('credits.html');
}
