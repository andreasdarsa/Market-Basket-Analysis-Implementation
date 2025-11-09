document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('csv-file');
    const messageDiv = document.getElementById('upload-message');

    const checkUploadsBtn = document.getElementById('check-uploads-btn');
    const uploadsInfoDiv = document.getElementById('uploads-info');

    checkUploadsBtn.addEventListener('click', async () => {
        uploadsInfoDiv.innerHTML = '';
        try {
            const response = await fetch('/api/file_info', {
                method: 'GET'
            });
            const data = await response.json();

            if (response.ok) {
                if (data.file_name) {
                    uploadsInfoDiv.innerHTML = `<div class="alert alert-info"><strong>Uploaded File:</strong> <span>${data.file_name}</span></div>`;
                } else {
                    uploadsInfoDiv.innerHTML = '<div class="alert alert-info">No files have been uploaded yet.</div>';
                }
            } else {
                uploadsInfoDiv.innerHTML = `<div class="alert alert-danger">${data.error || 'Failed to fetch uploads.'}</div>`;
            }
        } catch (error) {
            uploadsInfoDiv.innerHTML = '<div class="alert alert-danger">An error occurred while fetching uploads.</div>';
            console.error(error);
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        messageDiv.innerHTML = '';
        if (!file) {
            messageDiv.innerHTML = '<div class="alert alert-warning">Please select a file to upload.</div>';
            return;
        }

        const formData = new FormData();
        formData.append('csvFile', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                messageDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            } else {
                messageDiv.innerHTML = `<div class="alert alert-danger">${data.error || 'Upload failed.'}</div>`;
            }
        } catch (error) {
            messageDiv.innerHTML = '<div class="alert alert-danger">An error occurred while uploading the file.</div>';
            console.error(error);
        }
    });
});
