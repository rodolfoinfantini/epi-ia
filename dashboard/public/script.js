const API = {
    page: 1,
    size: 15,
    hasNext: true,
    async fetchNext() {
        if (!this.hasNext) return null;
        const res = await fetch(`alerts?page=${this.page}&size=${this.size}`);
        const data = await res.json();
        this.hasNext = data.hasNext;
        this.page++;
        return data.alerts;
    },
    reset() {
        this.page = 1;
        this.hasNext = true;
    }
};

const translations = { Glasses: 'Óculos', Helmet: 'Capacete' };
const sectionsEl = document.getElementById('sections');
const loadingEl = document.getElementById('loading');
const contentEl = document.querySelector('.content');

let loading = false;
const sectionsMap = new Map();

function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}
function formatTime(iso) {
    const d = new Date(iso);
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

async function loadStats() {
    const res = await fetch('http://localhost:3000/quick-stats');
    const stats = await res.json();

    const quickStatsEl = document.getElementById('quick-stats');
    quickStatsEl.innerHTML = ''; // limpa conteúdo anterior

    const title = document.createElement('h2');
    title.textContent = 'Ocorrências hoje';
    quickStatsEl.appendChild(title);

    const statsContainer = document.createElement('div');
    statsContainer.className = 'stats-container';

    // Card de Total
    const totalDiv = document.createElement('div');
    totalDiv.className = 'stat-card';

    const totalLabel = document.createElement('div');
    totalLabel.textContent = 'Total';

    const totalCount = document.createElement('span');
    totalCount.textContent = stats.total;

    totalDiv.appendChild(totalLabel);
    totalDiv.appendChild(totalCount);
    statsContainer.appendChild(totalDiv);

    // Cards individuais por classe
    for (const cls in stats.classes) {
        const div = document.createElement('div');
        div.className = 'stat-card';

        const label = document.createElement('div');
        label.textContent = translations[cls] || cls;

        const count = document.createElement('span');
        count.textContent = stats.classes[cls];

        div.appendChild(label);
        div.appendChild(count);
        statsContainer.appendChild(div);
    }

    quickStatsEl.appendChild(statsContainer);
}

function renderAlerts(alerts) {
    alerts.forEach(a => {
        const day = formatDate(a.timestamp);
        let sec = sectionsMap.get(day);
        if (!sec) {
            sec = document.createElement('section');
            sec.className = 'section';
            const h3 = document.createElement('h3');
            h3.textContent = day;
            sec.appendChild(h3);
            sectionsEl.appendChild(sec);
            sectionsMap.set(day, sec);
        }
        const card = document.createElement('div');
        card.className = 'card';

        const img = document.createElement('img');
        img.src = a.thumb;
        img.alt = translations[a.class] || a.class;
        card.appendChild(img);

        const info = document.createElement('div');
        info.className = 'info';
        const pClass = document.createElement('p');
        pClass.textContent = translations[a.class] || a.class;
        info.appendChild(pClass);
        const pTime = document.createElement('p');
        pTime.className = 'time';
        pTime.textContent = formatTime(a.timestamp);
        info.appendChild(pTime);
        card.appendChild(info);

        const actions = document.createElement('div');
        actions.className = 'actions';
        const btn = document.createElement('button');
        btn.textContent = 'Ver vídeo';
        btn.onclick = () => {
            const modalVideo = document.getElementById('modal-video');
            document.getElementById('modal').classList.remove('hidden');
            modalVideo.src = a.record;
        };
        actions.appendChild(btn);
        card.appendChild(actions);

        sec.appendChild(card);
    });
}

async function loadMore() {
    if (loading || !API.hasNext) return;
    loading = true;
    loadingEl.style.display = 'block';
    const alerts = await API.fetchNext();
    if (alerts && alerts.length) renderAlerts(alerts);
    loadingEl.style.display = 'none';
    loading = false;
}

function refreshAll() {
    API.reset();
    sectionsMap.clear();
    sectionsEl.innerHTML = '';
    contentEl.scrollTop = 0;
    loadStats();
    loadMore();
}

// infinite scroll
contentEl.addEventListener('scroll', () => {
    if (contentEl.scrollTop + contentEl.clientHeight >= contentEl.scrollHeight - 100) {
        loadMore();
    }
});

// modal close
document.getElementById('modal-close').onclick = () => {
    document.getElementById('modal').classList.add('hidden');
    document.getElementById('modal-video').pause();
};

// sidebar buttons
document.getElementById('btn-occurrences').onclick = () => { };
document.getElementById('btn-statistics').onclick = () => {
    alert('Estatísticas não implementado');
};

// init
loadStats();
loadMore();
// a cada 5 minutos, recarrega toda a lista
setInterval(refreshAll, 3 * 60 * 1000);

