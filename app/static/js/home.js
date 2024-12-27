function toggleText(button) {
    const cardBody = button.parentElement;
    const fullText = cardBody.querySelector('.full-text');

    if (fullText.style.display == "none") {
        fullText.style.display = "block";
        button.textContent = "Свернуть";
    } else {
        fullText.style.display = "none";
        button.textContent = "Открыть";
    }
}