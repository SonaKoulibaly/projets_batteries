// Configuration
const API_URL = 'https://ona6-battery-soh-api.hf.space';

// Variables globales
let uploadedData = null;
let predictions = null;
let chart = null;

// Éléments DOM
const csvFile = document.getElementById('csvFile');
const dataPreview = document.getElementById('dataPreview');
const previewTable = document.getElementById('previewTable');
const predictBtn = document.getElementById('predictBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorDiv = document.getElementById('error');
const downloadBtn = document.getElementById('downloadBtn');

// Event Listeners
csvFile.addEventListener('change', handleFileUpload);
predictBtn.addEventListener('click', makePrediction);
downloadBtn.addEventListener('click', downloadResults);

/**
 * Gérer l'upload du fichier CSV
 */
function handleFileUpload(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
        showError('❌ Veuillez uploader un fichier CSV');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function(e) {
        try {
            const text = e.target.result;
            const data = parseCSV(text);
            
            if (data.length < 20) {
                showError(`❌ Minimum 20 mesures requises. Vous avez uploadé ${data.length} mesures.`);
                predictBtn.disabled = true;
                return;
            }
            
            // Vérifier les colonnes requises
            const requiredCols = ['Voltage_measured', 'Current_measured', 'Temperature_measured', 'SoC', 'cycle_number'];
            const missingCols = requiredCols.filter(col => !data[0].hasOwnProperty(col));
            
            if (missingCols.length > 0) {
                showError(`❌ Colonnes manquantes: ${missingCols.join(', ')}`);
                predictBtn.disabled = true;
                return;
            }
            
            uploadedData = data;
            displayPreview(data);
            predictBtn.disabled = false;
            hideError();
            
        } catch (error) {
            showError('❌ Erreur lors de la lecture du fichier: ' + error.message);
        }
    };
    
    reader.readAsText(file);
}

/**
 * Parser CSV en tableau d'objets
 */
function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        
        headers.forEach((header, index) => {
            row[header] = isNaN(values[index]) ? values[index] : parseFloat(values[index]);
        });
        
        data.push(row);
    }
    
    return data;
}

/**
 * Afficher l'aperçu des données
 */
function displayPreview(data) {
    const preview = data.slice(0, 5); // Afficher 5 premières lignes
    
    let html = '<table class="min-w-full text-slate-300">';
    html += '<thead><tr class="border-b border-slate-700">';
    
    Object.keys(preview[0]).forEach(key => {
        html += `<th class="px-4 py-2 text-left">${key}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    preview.forEach(row => {
        html += '<tr class="border-b border-slate-800">';
        Object.values(row).forEach(value => {
            html += `<td class="px-4 py-2">${typeof value === 'number' ? value.toFixed(2) : value}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    html += `<p class="text-slate-400 mt-2 text-xs">Affichage de 5/${data.length} lignes</p>`;
    
    previewTable.innerHTML = html;
    dataPreview.classList.remove('hidden');
}

/**
 * Faire la prédiction
 */
async function makePrediction() {
    if (!uploadedData) return;
    
    // Afficher le loading
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    hideError();
    predictBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: uploadedData })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erreur serveur');
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error('Échec de la prédiction');
        }
        
        predictions = result.predictions;
        displayResults(result);
        
    } catch (error) {
        showError('❌ Erreur: ' + error.message);
        console.error('Erreur:', error);
    } finally {
        loading.classList.add('hidden');
        predictBtn.disabled = false;
    }
}

/**
 * Afficher les résultats
 */
function displayResults(result) {
    const stats = result.statistics;
    
    // Afficher les statistiques
    document.getElementById('meanSoH').textContent = stats.mean.toFixed(2) + '%';
    document.getElementById('minSoH').textContent = stats.min.toFixed(2) + '%';
    document.getElementById('maxSoH').textContent = stats.max.toFixed(2) + '%';
    
    // Créer le graphique
    createChart(result.predictions);
    
    // Afficher la section résultats
    results.classList.remove('hidden');
    
    // Scroll vers les résultats
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Créer le graphique des prédictions
 */
function createChart(predictions) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    // Détruire l'ancien graphique si existe
    if (chart) {
        chart.destroy();
    }
    
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: predictions.map((_, i) => i + 1),
            datasets: [{
                label: 'SoH Prédit (%)',
                data: predictions,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: {
                            size: 14,
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    borderColor: '#10b981',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return 'SoH: ' + context.parsed.y.toFixed(2) + '%';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Échantillon',
                        color: '#cbd5e1',
                        font: {
                            size: 12,
                            family: "'Inter', sans-serif"
                        }
                    },
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'SoH (%)',
                        color: '#cbd5e1',
                        font: {
                            size: 12,
                            family: "'Inter', sans-serif"
                        }
                    },
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    }
                }
            }
        }
    });
}

/**
 * Télécharger les résultats
 */
function downloadResults() {
    if (!predictions) return;
    
    let csv = 'Echantillon,SoH_Predit\n';
    predictions.forEach((pred, i) => {
        csv += `${i + 1},${pred.toFixed(4)}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'predictions_soh.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * Afficher une erreur
 */
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

/**
 * Masquer l'erreur
 */
function hideError() {
    errorDiv.classList.add('hidden');
}

// Smooth scroll pour les liens de navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});