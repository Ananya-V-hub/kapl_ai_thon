from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simple in-memory storage
data_storage = []

# HTML page with interactive JavaScript (simulates React-like behavior)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Energy Optimizer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: auto; }
        input { display: block; margin: 10px 0; padding: 8px; width: 300px; }
        button { padding: 10px 20px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Dynamic Energy Optimizer</h1>

    <h2>Input Energy Data</h2>
    <input type="text" id="appliance" placeholder="Appliance">
    <input type="number" step="0.01" id="powerUsage" placeholder="Power Usage (kWh)">
    <input type="number" step="0.01" id="usageTime" placeholder="Usage Time (hrs)">
    <input type="number" step="0.01" id="billAmount" placeholder="Bill Amount ($)">
    <input type="number" step="0.01" id="temperature" placeholder="Temperature (°C)">
    <button onclick="submitData()">Submit</button>

    <h2>Energy Insights</h2>
    <p><strong>Peak Hours:</strong> <span id="peakHours">Loading...</span></p>
    <h3>Suggestions:</h3>
    <ul id="suggestionsList"></ul>

    <h2>Bill Visualization</h2>
    <canvas id="billChart" width="400" height="200"></canvas>

    <script>
        function submitData() {
            const data = {
                appliance: document.getElementById('appliance').value,
                powerUsage: parseFloat(document.getElementById('powerUsage').value),
                usageTime: parseFloat(document.getElementById('usageTime').value),
                billAmount: parseFloat(document.getElementById('billAmount').value),
                temperature: parseFloat(document.getElementById('temperature').value)
            };

            fetch('/submit-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                alert('Data submitted successfully!');
                loadInsights();
                loadChart();
            });
        }

        function loadInsights() {
            fetch('/predict')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('peakHours').innerText = data.peak_hours.join(', ');
                    document.getElementById('suggestionsList').innerHTML = data.suggestions.map(s => `<li>${s}</li>`).join('');
                });
        }

        function loadChart() {
            fetch('/get-visualization')
                .then(res => res.json())
                .then(data => {
                    const ctx = document.getElementById('billChart').getContext('2d');
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: 'Bill Amount ($)',
                                data: data.values,
                                backgroundColor: 'rgba(75, 192, 192, 0.6)'
                            }]
                        }
                    });
                });
        }

        window.onload = () => {
            loadInsights();
            loadChart();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.json
    data_storage.append(data)
    return jsonify({"message": "Data saved successfully!"})

@app.route('/predict', methods=['GET'])
def predict():
    # Simulated prediction logic
    peak_hours = ["6 PM - 9 PM"]
    suggestions = ["Run Washing Machine after 10 PM", "Use AC between 1 PM - 3 PM"]
    return jsonify({"peak_hours": peak_hours, "suggestions": suggestions})

@app.route('/get-visualization', methods=['GET'])
def get_visualization():
    labels = ["Jan", "Feb", "Mar"]
    values = [2000, 1800, 2200]
    return jsonify({"labels": labels, "values": values})

if __name__ == '__main__':
    app.run(debug=True)
