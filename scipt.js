document.querySelectorAll('.neon-text').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.style.textShadow = "0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff";
    });
    item.addEventListener('mouseout', () => {
        item.style.textShadow = "0 0 5px #0ff, 0 0 10px #0ff, 0 0 20px #0ff";
    });
});
