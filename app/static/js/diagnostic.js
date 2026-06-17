document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return;
            fetch('/api/search?q=' + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('results');
                    resultsDiv.innerHTML = '';
                    if (data.results.length === 0) {
                        resultsDiv.innerHTML = '<p>No se encontraron resultados.</p>';
                        if (data.suggestions && data.suggestions.length > 0) {
                            document.getElementById('suggestions').innerHTML = '<p>¿Quisiste decir: ' + data.suggestions.join(', ') + '?</p>';
                        }
                        return;
                    }
                    data.results.forEach(function(item) {
                        const col = document.createElement('div');
                        col.className = 'col-4';
                        col.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h5>${item.name}</h5>
                                    <p>${item.description ? item.description.substring(0, 100) : ''}</p>
                                    <a href="/aveologia/disease/${item.id}" class="btn btn-primary btn-sm">Ver más</a>
                                </div>
                            </div>
                        `;
                        resultsDiv.appendChild(col);
                    });
                    document.getElementById('suggestions').innerHTML = '';
                })
                .catch(() => {});
        });
    }

    const diagnosticBtn = document.getElementById('diagnosticBtn');
    if (diagnosticBtn) {
        diagnosticBtn.addEventListener('click', function() {
            const symptoms = document.getElementById('symptomsInput').value.split(',').map(s => s.trim()).filter(Boolean);
            if (!symptoms.length) return;
            fetch('/api/diagnostic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptoms: symptoms })
            })
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('diagnosticResults');
                resultsDiv.innerHTML = '';
                if (data.results.length === 0) {
                    resultsDiv.innerHTML = '<p>No se encontraron coincidencias.</p>';
                    return;
                }
                data.results.forEach(function(item) {
                    const col = document.createElement('div');
                    col.className = 'col-6';
                    col.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <h5>${item.disease}</h5>
                                <p>${item.description ? item.description.substring(0, 100) : ''}</p>
                                <p><strong>Tratamiento:</strong> ${item.treatment || 'No especificado'}</p>
                                <p><strong>Coincidencia:</strong> ${item.score}%</p>
                            </div>
                        </div>
                    `;
                    resultsDiv.appendChild(col);
                });
            })
            .catch(() => {});
        });
    }
});