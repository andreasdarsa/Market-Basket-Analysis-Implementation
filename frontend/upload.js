document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('csv-file');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a CSV file.');
            return;
        }

        const formData = new FormData();
        formData.append('csv', file);

        try {
            const response = await fetch('/upload_csv', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                alert('Upload successful!');
                // Optionally handle result
            } else {
                alert('Upload failed.');
            }
        } catch (error) {
            alert('Error uploading file.');
            console.error(error);
        }
    });
});