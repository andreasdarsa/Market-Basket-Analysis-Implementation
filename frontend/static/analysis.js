// Once the user clicks 'Submit' on the analysis page, request the apriori result (rules)
document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default form submission
        fetchAprioriResults();
    });
});

function fetchAprioriResults() {
    // Get form values
    const minSupport = document.getElementById('minSupport').value;
    const minConfidence = document.getElementById('minConfidence').value;
    const minLift = document.getElementById('minLift').value;
    const payload = {
        minSupport: parseFloat(minSupport),
        minConfidence: parseFloat(minConfidence),
        minLift: parseFloat(minLift)
    };
    // Send POST request to the server
    fetch('/api/rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        displayAprioriResults(data);
    })
    .catch(error => {
        console.error('Error fetching apriori results:', error);
    });
}

function displayAprioriResults(data) {
    const resultsDiv = document.getElementById('results-table-container');
    resultsDiv.innerHTML = ''; // Clear previous results
    if (data.error) {
        resultsDiv.innerHTML = `<p class="text-danger">${data.error}</p>`;
        return;
    }
    if (data.length === 0) {
        resultsDiv.innerHTML = '<p>No association rules found with the given parameters.</p>';
        return;
    }
    let tableHTML = '<table class="table table-bordered"><thead><tr>';
    // Table headers
    Object.keys(data[0]).forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';
    // Table rows
    data.forEach(row => {
        tableHTML += '<tr>';
        Object.values(row).forEach(value => {
            tableHTML += `<td>${value}</td>`;
        });
        tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table>';
    resultsDiv.innerHTML = tableHTML;
}
