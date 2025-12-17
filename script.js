(function () {
    const nextBtn = document.getElementById('next-section-btn');
    const prevBtn = document.getElementById('prev-section-btn');
    const searchFocusBtn = document.getElementById('search-focus-btn');
    const buttonSection = document.querySelector('.button-section');
    const categoryNav = document.querySelector('.category-nav');
    const sections = Array.from(document.querySelectorAll('section.category-section'));
    const footer = document.querySelector('.site-footer');
    if ((!nextBtn && !prevBtn && !searchFocusBtn) || sections.length === 0) return;

    function currentIndex() {
        const mid = window.innerHeight / 3;
        let idx = sections.findIndex(s => {
            const r = s.getBoundingClientRect();
            return r.top <= mid && r.bottom > mid;
        });
        if (idx === -1) {
            // fallback: nearest to top
            let min = Infinity; idx = 0;
            sections.forEach((s, i) => { const d = Math.abs(s.getBoundingClientRect().top); if (d < min) { min = d; idx = i; } });
        }
        return idx;
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            const i = currentIndex();
            const next = sections[(i + 1) % sections.length];
            if (next) next.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            const i = currentIndex();
            const prev = sections[(i - 1 + sections.length) % sections.length];
            if (prev) prev.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    if (searchFocusBtn) {
        searchFocusBtn.addEventListener('click', () => {
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                searchInput.focus();
            }
        });
    }

    // hide buttons if only one section
    if (sections.length <= 1) {
        if (buttonSection) buttonSection.style.display = 'none';
    }

    // Hide buttons when footer is visible
    if (footer) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const visible = entry.isIntersecting;
                if (buttonSection) buttonSection.style.display = visible ? 'none' : '';
            });
        }, { threshold: 0.1 }); // Trigger when 10% of footer is visible
        observer.observe(footer);
    }

    // Search functionality
    const searchInput = document.getElementById('search-input');
    const cards = Array.from(document.querySelectorAll('.card'));
    const categoryHeaders = document.querySelectorAll('.category-header');
    const main = document.querySelector('main');
    const searchResults = document.getElementById('search-results');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query) {
                if (categoryNav) categoryNav.classList.add('hidden-by-search');
                if (buttonSection) buttonSection.classList.add('hidden-by-search');
                // Hide main and show search results
                main.style.display = 'none';
                searchResults.style.display = 'grid';
                // Clear previous results
                searchResults.innerHTML = '';
                // Filter and append matching cards
                cards.forEach(card => {
                    const title = card.querySelector('.card-title').textContent.toLowerCase();
                    if (title.includes(query)) {
                        const clone = card.cloneNode(true);
                        searchResults.appendChild(clone);
                    }
                });
                // If no results, show message
                if (searchResults.children.length === 0) {
                    const noResults = document.createElement('p');
                    noResults.textContent = 'Item não encontrado!';
                    noResults.style.textAlign = 'center';
                    noResults.style.fontSize = '18px';
                    noResults.style.color = '#666';
                    noResults.style.gridColumn = '1 / -1'; // Span full width in grid
                    searchResults.appendChild(noResults);
                }
            } else {
                if (categoryNav) categoryNav.classList.remove('hidden-by-search');
                if (buttonSection) buttonSection.classList.remove('hidden-by-search');
                // Show main and hide search results
                main.style.display = '';
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
            }
        });
    }
})();