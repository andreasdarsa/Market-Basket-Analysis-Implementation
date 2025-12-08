// Add heatmap visualization
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/visualize/heatmap')
        .then(response => response.json())
        .then(data => {
            if (data.image) {
                const img = document.createElement('img');
                img.src = 'data:image/png;base64,' + data.image;
                img.alt = 'Heatmap Visualization';
                document.getElementById('graph-heatmap-container').appendChild(img);
            } else {
                console.error('No image data received for heatmap.');
            }
        })
        .catch(error => console.error('Error fetching heatmap visualization:', error));
});

// Add frequent items visualization
document.addEventListener('DOMContentLoaded', function() {
    const n = 10; // Number of top frequent items to display
    fetch(`/api/visualize/frequent_items?n=${n}`) // Adjust the endpoint as necessary
        .then(response => response.json())
        .then(data => {
            if (data.image) {
                const img = document.createElement('img');
                img.src = 'data:image/png;base64,' + data.image;
                img.alt = 'Frequent Items Visualization';
                document.getElementById('graph-frequent-items-container').appendChild(img);
            } else {
                console.error('No image data received for frequent items.');
            }
        })
        .catch(error => console.error('Error fetching frequent items visualization:', error));
});

// Add rules network visualization
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/visualize/rules_network') // Adjust the endpoint as necessary
        .then(response => response.json())
        .then(data => {
            if (data.image) {
                const img = document.createElement('img');
                img.src = 'data:image/png;base64,' + data.image;
                img.alt = 'Rules Network Visualization';
                document.getElementById('graph-network-container').appendChild(img);
            } else {
                console.error('No image data received for rules network.');
            }
        })
        .catch(error => console.error('Error fetching rules network visualization:', error));
});

// Add scatter plot visualization
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/visualize/scatter_lift_support') // Adjust the endpoint as necessary
        .then(response => response.json())
        .then(data => {
            if (data.image) {
                const img = document.createElement('img');
                img.src = 'data:image/png;base64,' + data.image;
                img.alt = 'Scatter Plot Visualization';
                document.getElementById('graph-scatter-container').appendChild(img);
            } else {
                console.error('No image data received for scatter plot.');
            }
        })
        .catch(error => console.error('Error fetching scatter plot visualization:', error));
});
