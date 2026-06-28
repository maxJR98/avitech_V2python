document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return;
            
            fetch('/aveologia/api/search?q=' + encodeURIComponent(query))
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
});