document.addEventListener("DOMContentLoaded", function() {
    let score = 0;
    const scoreElement = document.getElementById("score");
    const button = document.getElementById("click-button");

    button.addEventListener("click", function() {
        score++;
        scoreElement.textContent = score;
    });
});
