document.addEventListener("DOMContentLoaded", function() {
    let score = 0;
    let bute = 10;
    const scoreElement = document.getElementById("score");
    const button = document.getElementById("click-button");

    button.addEventListener("click", function() {
        score++;
        if (score == bute) {
            alert(`Score de ${bute} atteint`);
            bute *= 2;
        }
        scoreElement.textContent = score;
    });
});
