function redirectToUploadPage() {
    window.location.href = 'frontend/upload.html';
}

// Example: Attach to navbar link with id 'upload-link'
document.getElementById('upload-link').addEventListener('click', function(e) {
    e.preventDefault();
    redirectToUploadPage();
});