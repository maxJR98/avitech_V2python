document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('calculateBtn').addEventListener('click', function() {
        const geneticLine = document.getElementById('geneticLine').value.trim();
        const weeks = parseInt(document.getElementById('weeks').value);
        const birds = parseInt(document.getElementById('birds').value);
        
        if (!geneticLine || !weeks || !birds) {
            alert('Completa todos los campos.');
            return;
        }

        fetch('/calculadora/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ genetic_line: geneticLine, weeks: weeks, birds: birds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('feedResult').textContent = 'Error: ' + data.error;
                document.getElementById('waterResult').textContent = '';
                document.getElementById('phaseResult').textContent = '';
                return;
            }
            document.getElementById('feedResult').textContent = 'Alimento diario: ' + data.daily_feed_kg + ' kg';
            document.getElementById('waterResult').textContent = 'Agua diaria: ' + data.daily_water_l + ' L';
            document.getElementById('phaseResult').textContent = 'Fase recomendada: ' + (data.feed_phase || 'No especificada');
        })
        .catch(() => {});
    });
});