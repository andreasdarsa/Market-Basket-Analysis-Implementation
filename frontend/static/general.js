document.addEventListener('DOMContentLoaded', function() {

    // Make the "About" link show an alert with information about the app
    const aboutLink = document.querySelector('#toAbout');
    if (aboutLink) {
        aboutLink.addEventListener('click', function(event) {
            event.preventDefault();
            alert('Market Basket Analyzer\n\nThis application helps you analyze market basket data to find associations between products. It is built using Flask for the backend and Bootstrap for the frontend.\n\nDeveloped by Andreas Darsaklis.');
        });
    }
    

    // Toggle the navbar on small screens
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('#navbarContent');
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function () {
            navbarCollapse.classList.toggle('show');
        });
    }
});