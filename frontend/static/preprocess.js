document.addEventListener('DOMContentLoaded', function() {
    const fileInfoDiv = document.getElementById('file-info');

    // Αν χρησιμοποιούμε fetch για να πάρουμε info από backend
    fetch('/api/file_info')
        .then(res => res.json())
        .then(fileInfo => {
            if (fileInfo && fileInfo.fileName && typeof fileInfo.transactionCount === 'number') {
                fileInfoDiv.innerHTML = `
                    <p><strong>File Name:</strong> ${fileInfo.file_name}</p>
                    <p><strong>Number of Transactions:</strong> ${fileInfo.transaction_count}</p>
                `;
            } 
            else {
                fileInfoDiv.innerHTML = `<p>No file uploaded yet.</p>`;
            }
        });
    });

document.addEventListener('DOMContentLoaded', function() {
    const previewDiv = document.getElementById('cleaned-data-preview');

    // Αν χρησιμοποιούμε fetch για να πάρουμε το preview από backend
    fetch('/api/preprocess/preview')
        .then(res => res.json())
        .then(data => {
            if (data && data.length > 0) {
                let tableHTML = '<table class="table table-striped"><thead><tr>';
                // Headers
                Object.keys(data[0]).forEach(header => {
                    tableHTML += `<th>${header}</th>`;
                });
                tableHTML += '</tr></thead><tbody>';
                // Rows
                data.forEach(row => {
                    tableHTML += '<tr>';
                    Object.values(row).forEach(value => {
                        tableHTML += `<td>${value}</td>`;
                    });
                    tableHTML += '</tr>';
                });
                tableHTML += '</tbody></table>';
                previewDiv.innerHTML = tableHTML;
            } 
            else {
                previewDiv.innerHTML = '<p>No cleaned data available. Please preprocess a file first.</p>';
            }
        });
    });

document.addEventListener('DOMContentLoaded', function() {
    const summaryDiv = document.getElementById('data-summary');

    // Αν χρησιμοποιούμε fetch για να πάρουμε το summary από backend
    fetch('/api/preprocess/stats')
        .then(res => res.json())
        .then(summary => {
            if (summary) {
                let summaryHTML = '<ul>';
                for (const [key, value] of Object.entries(summary)) {
                    summaryHTML += `<li><strong>${key}:</strong> ${value}</li>`;
                }
                summaryHTML += '</ul>';
                summaryDiv.innerHTML = summaryHTML;
            } else {
                summaryDiv.innerHTML = '<p>No summary available. Please preprocess a file first.</p>';
            }
        });
});
