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
    document.getElementById("popupOverlay").querySelector("form").reset(); // Réinitialiser le formulaire
}

// Afficher la popup après 5 minutes
setTimeout(() => {
    document.getElementById('overlay').style.display = 'flex';
}, 300000); // 5 minutes en millisecondes (300000 ms)

// Fonction pour téléporter un élément à une position aléatoire sur la page
function teleportElement(element) {
    const randomX = Math.random() * (window.innerWidth - 50);
    const randomY = Math.random() * (window.innerHeight - 50);

    element.style.position = 'absolute';
    element.style.left = `${randomX}px`;
    element.style.top = `${randomY}px`;
}

// Ajouter un événement de survol pour déplacer les labels (ronds)
const ratingLabels = document.querySelectorAll('.rating-container label');

ratingLabels.forEach(label => {
    label.addEventListener('mouseenter', function() {
        const input = document.getElementById(this.getAttribute('for'));
        if (input.value !== '5') {
            teleportElement(this);
        }
    });
});

// Activer le bouton de confirmation seulement si la note 5 est sélectionnée
const ratingForm = document.getElementById('rating-form');
const submitButton = document.getElementById('submit-btn');

ratingForm.addEventListener('change', function() {
    submitButton.disabled = !document.getElementById('rate-5').checked;
});

// Fermer la popup si la note 5 est sélectionnée et soumettre le formulaire
ratingForm.addEventListener('submit', function(event) {
    event.preventDefault();
    if (document.getElementById('rate-5').checked) {
        document.getElementById('overlay').style.display = 'none';
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#popupOverlay form");

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            const formData = new FormData(form);

            try {
                const response = await fetch("http://localhost:5000/envoie", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) throw new Error("Erreur lors de l'envoi");

                const data = await response.json();
                console.log("Réponse du serveur:", data);

                closePopup();
            } catch (error) {
                console.error(error);
            }
        });
    }
});
