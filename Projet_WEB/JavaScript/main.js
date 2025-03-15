// Sélectionner tous les boutons ayant la classe 'bouton-achat'
var boutons = document.querySelectorAll('.bouton-achat');

// Ajouter les écouteurs d'événements sur chaque bouton
boutons.forEach(function(bouton) {
    bouton.addEventListener('mouseover', function() {
        changerCouleur(bouton, true);
    });
    bouton.addEventListener('mouseout', function() {
        changerCouleur(bouton, false);
    });
});

function changerCouleur(bouton, survol) {
    if (survol) {
        bouton.style.backgroundColor = 'white';
        bouton.style.color = 'rgba(134, 212, 69, 0.9)';
        bouton.style.border = '2px solid rgba(134, 212, 69, 0.9)';
    } else {
        bouton.style.backgroundColor = 'rgba(134, 212, 69, 0.9)';
        bouton.style.color = 'white';
        bouton.style.border = 'none';
    }
}

function openPopup() {
    document.getElementById("popupOverlay").style.display = "flex";
}

function closePopup() {
    document.getElementById("popupOverlay").style.display = "none";
}

// Afficher la popup après 5 minutes
setTimeout(() => {
    document.getElementById('overlay').style.display = 'flex';
}, 300000); // 5 minutes en millisecondes (300000 ms)

// Fonction pour téléporter un élément à une position aléatoire sur la page
function teleportElement(element) {
    // Calculer une position aléatoire dans la fenêtre
    const randomX = Math.random() * (window.innerWidth - 50);  // 50 est la taille du rond
    const randomY = Math.random() * (window.innerHeight - 50); // 50 est la taille du rond

    // Appliquer la position aléatoire à l'élément
    element.style.position = 'absolute';
    element.style.left = `${randomX}px`;
    element.style.top = `${randomY}px`;
}

// Ajouter un événement de survol pour déplacer les ronds
const ratingInputs = document.querySelectorAll('.rating-container input');

ratingInputs.forEach(input => {
    input.addEventListener('mouseenter', function() {
        if (this.value != '5') {
            // Téléporter immédiatement le rond
            teleportElement(this);
        }
    });
});

// Activer le bouton de confirmation seulement si la note 5 est sélectionnée
const ratingForm = document.getElementById('rating-form');
const submitButton = document.getElementById('submit-btn');

ratingForm.addEventListener('change', function() {
    if (document.getElementById('rate-5').checked) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
});

// Fermer la popup si la note 5 est sélectionnée et soumettre le formulaire
ratingForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche l'envoi du formulaire réel
    if (document.getElementById('rate-5').checked) {
        document.getElementById('overlay').style.display = 'none'; // Fermer la popup
    }
});

