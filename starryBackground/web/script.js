document.addEventListener('mousemove', (e) => {
    const stars = document.querySelectorAll('#stars, #stars2, #stars3');
    const moveX = (e.clientX - window.innerWidth / 2) * 0.02;
    const moveY = (e.clientY - window.innerHeight / 2) * 0.02;

    // TODO: some thing
    
    stars.forEach((star, index) => {
        star.style.transform = `translate(${moveX * (index + 1)}px, ${moveY * (index + 1)}px)`;
    });
});
