// helper para criar <canvas>
function makeCanvas(id, title) {
    const container = document.getElementById('stats-container');
    const wrapper = document.createElement('div');
    wrapper.className = 'chart-wrapper';
    const h3 = document.createElement('h3');
    h3.textContent = title;
    const canvas = document.createElement('canvas');
    canvas.id = id;
    wrapper.append(h3, canvas);
    container.appendChild(wrapper);
    return canvas.getContext('2d');
}

async function fetchJSON(url) {
    try {
        const res = await fetch(url, { headers: { Authorization: `Bearer ${localStorage.token}` } });
        return res.json();
    } catch (err) {
        location.href = '/login';
    }
}

async function drawDaily() {
    const { labels, series } = await fetchJSON('/stats/daily');
    const ctx = makeCanvas('chart-daily', 'Alertas por Dia (últimos 30d)');
    new Chart(ctx, {
        type: 'line',
        data: { labels, datasets: [{ label: 'Alertas/dia', data: series, borderColor: '#bb86fc', fill: false }] },
        options: { scales: { x: { ticks: { color: '#eee' } }, y: { ticks: { color: '#eee' } } } }
    });
}

async function drawClasses() {
    const { labels, series } = await fetchJSON('/stats/classes');
    const ctx = makeCanvas('chart-classes', 'Total por Classe (30d)');
    new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Alertas', data: series, backgroundColor: '#03dac6' }] },
        options: { indexAxis: 'y', scales: { x: { ticks: { color: '#eee' } }, y: { ticks: { color: '#eee' } } } }
    });
}

async function drawHourly() {
    const { labels, series } = await fetchJSON('/stats/hourly');
    const ctx = makeCanvas('chart-hourly', 'Distribuição Horária (7d)');
    new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Alertas', data: series, backgroundColor: '#fbbc05' }] },
        options: { scales: { x: { ticks: { color: '#eee' } }, y: { ticks: { color: '#eee' } } } }
    });
}

async function drawHeatmap() {
    const { days, classes, matrix } = await fetchJSON('/stats/heatmap');
    const data = [];
    classes.forEach((cls, i) => {
        matrix[i].forEach((val, j) => {
            data.push({ x: days[j], y: cls, v: val });
        });
    });
    const ctx = makeCanvas('chart-heatmap', 'Heatmap Dia × Classe (30d)');
    new Chart(ctx, {
        type: 'matrix',
        data: {
            datasets: [{
                label: 'Alertas',
                data,
                backgroundColor: context => {
                    const val = context.dataset.data[context.dataIndex].v;
                    if (val === 0) {
                        // nenhuma cor (totalmente transparente)
                        return 'rgba(0,0,0,0)';
                    }
                    const max = Math.max(...data.map(d => d.v), 1);
                    const alpha = val / max;
                    return `rgba(187,134,252,${alpha})`;
                },
                borderWidth: 1,
                borderColor: 'rgba(255,255,255,0.1)',
            }]
        },
        options: {
            scales: {
                x: { type: 'category', labels: days, ticks: { color: '#eee' } },
                y: { type: 'category', labels: classes, ticks: { color: '#eee' } }
            },
            plugins: { legend: { display: false } }
        }
    });

}

window.addEventListener('DOMContentLoaded', () => {
    drawDaily();
    drawClasses();
    drawHourly();
    drawHeatmap();
});
