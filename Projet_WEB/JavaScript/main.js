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