// JavaScript for Navigation and Interactions

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Dynamic content loading example
    async function loadData(url, elementId) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            document.getElementById(elementId).innerHTML = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    // Example usage: loadData('/api/sensors', 'sensor-list');
});