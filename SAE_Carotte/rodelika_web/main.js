document.addEventListener('DOMContentLoaded', function () {
    // Attacher les événements aux boutons après le chargement du DOM
    document.getElementById('listStudentsBtn').addEventListener('click', listStudents);
    document.getElementById('studentBalancesBtn').addEventListener('click', studentBalances);
    document.getElementById('newStudentFormBtn').addEventListener('click', newstudents);
    document.getElementById('assignBonusFormBtn').addEventListener('click', assignBonusForm);
    document.getElementById('showCreditsBtn').addEventListener('click', showCredits);
});

// ...

function login() {
    var utilisateur = prompt("Entrez votre nom d'utilisateur:");
    var motdepasse = prompt("Entrez votre mot de passe:");

    var formData = new FormData();
    formData.append('utilisateur', utilisateur);
    formData.append('motdepasse', motdepasse);

    var responsePromise = fetch('login.php', {
        method: 'POST',
        body: formData
    });

    responsePromise
        .then(response => response.json())
        .then(data => {
            var decodedMessage = decodeURIComponent(data.message);
            alert(decodedMessage); // Afficher le message dans une pop-up

            if (data.success) {
                // Rediriger vers la page principale après l'authentification réussie
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error('Erreur lors de l\'authentification:', error));
}

// ...



function listStudents() {
    loadContent('list_students.php');
}

function studentBalances() {
    loadContent('student_balances.php');
}

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
            alert(decodedMessage); // Afficher le message dans une pop-up

            if (data.success) {
                // Rediriger vers la page principale après la pop-up
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error('Erreur lors de la création de l\'étudiant:', error));
}



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
            alert(decodedMessage); // Afficher le message dans une pop-up

            if (data.success) {
                // Rediriger vers la page principale après la pop-up
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error('Erreur lors de l\'attribution du bonus:', error));
}

function showCredits() {
    loadContent('credits.html');
}

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

