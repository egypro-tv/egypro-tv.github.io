let movies = [];
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultBox = document.getElementById('searchResults');

// 📥 تحميل ملف الأفلام من GitHub مباشرة
async function loadMovies() {
  const url =
    'https://raw.githubusercontent.com/egypro-tv/egypro-tv.github.io/refs/heads/main/movies.json';

  try {
    const response = await fetch(url, { cache: "no-store" });

    if (!response.ok) {
      throw new Error("Failed to load movies.json");
    }

    movies = await response.json();
    console.log('✅ Loaded movies.json from GitHub');
  } catch (err) {
    console.error('❌ Error loading movies.json:', err);
  }
}

loadMovies();

function searchMovies() {
  const searchTerm = searchInput.value.toLowerCase().trim();
  resultBox.innerHTML = '';

  if (searchTerm === '') {
    resultBox.style.display = 'none';
    return;
  }

  const searchWords = searchTerm.split(/\s+/);

  const filtered = movies
    .map(movie => {
      const title = movie.title.toLowerCase();
      const year = String(movie.year).toLowerCase();

      let score = 0;

      searchWords.forEach(word => {
        const titleWords = title.split(/\s+/);

        // 🔹 مطابقة كلمة كاملة
        if (titleWords.includes(word)) {
          score += 3; // أقوى تطابق
        }

        // 🔹 لو العنوان يبدأ بالكلمة
        if (title.startsWith(word)) {
          score += 2;
        }

        // 🔹 لو السنة مطابقة
        if (year === word) {
          score += 2;
        }
      });

      return { movie, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score); // ترتيب حسب القوة

  if (filtered.length === 0) {
    resultBox.style.display = 'block';
    resultBox.innerHTML = `<p class="no-results">لا توجد نتائج</p>`;
    return;
  }

  resultBox.style.display = 'block';

  const isSubPage = window.location.pathname.split('/').length > 3;

  filtered.forEach(item => {
    const movie = item.movie;

    const movieUrl = movie.url.startsWith('/') ? movie.url : '/' + movie.url;

    let posterUrl = movie.poster;
    if (!posterUrl.startsWith('/')) {
      posterUrl = '/' + posterUrl;
    }

    const div = document.createElement('div');
    div.classList.add('search-item');

    if (!isSubPage) {
      div.innerHTML = `
        <img src="${posterUrl}" alt="${movie.title}" class="search-thumb">
        <span>${movie.title}</span>
      `;
    } else {
      div.innerHTML = `<span>${movie.title}</span>`;
    }

    div.onclick = () => {
      location.href = movieUrl;
    };

    resultBox.appendChild(div);
  });
}


// الأحداث
searchBtn.addEventListener('click', searchMovies);
searchInput.addEventListener('keyup', searchMovies);

// 🔹 إخفاء القائمة عند الضغط خارج مربع البحث
document.addEventListener('click', (e) => {
  if (!e.target.closest('.search-bar')) {
    resultBox.style.display = 'none';
  }
});
