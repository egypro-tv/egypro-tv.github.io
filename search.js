let movies = [];
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultBox = document.getElementById('searchResults');

// 📥 تحميل ملف الأفلام
async function loadMovies() {
  const paths = [
    '/movies.json',
    '../movies.json',
    '../../movies.json',
    './movies.json'
  ];

  for (const path of paths) {
    try {
      const response = await fetch(path);
      if (response.ok) {
        movies = await response.json();
        console.log('✅ Loaded from:', path);
        return;
      }
    } catch (e) {}
  }

  console.error('❌ movies.json not found in any path');
}

loadMovies();

// 🧠 البحث
function searchMovies() {
  const searchTerm = searchInput.value.toLowerCase().trim();
  resultBox.innerHTML = '';

  if (searchTerm === '') {
    resultBox.style.display = 'none';
    return;
  }

  const searchWords = searchTerm.split(/\s+/);

  // 🔹 فلترة حسب title أو year
  const filtered = movies.filter(movie => {
    const title = movie.title.toLowerCase();
    const year = movie.year.toLowerCase(); // لو year string

    return searchWords.some(word => title.includes(word) || year.includes(word));
  });

  if (filtered.length === 0) {
    resultBox.style.display = 'block';
    resultBox.innerHTML = `<p class="no-results">لا توجد نتائج</p>`;
    return;
  }

  resultBox.style.display = 'block';

  // 🔍 هل الصفحة داخل مجلد فرعي؟
  const isSubPage = window.location.pathname.split('/').length > 3;

  filtered.forEach(movie => {
    const item = document.createElement('div');
    item.classList.add('search-item');

    // 🔗 تصحيح رابط الفيلم
    const movieUrl = movie.url.startsWith('/') ? movie.url : '/' + movie.url;

    // 🖼️ تصحيح مسار الصورة
    let posterUrl = movie.poster;
    if (!posterUrl.startsWith('/')) {
      posterUrl = '/' + posterUrl;
    }

    // العرض حسب مكان الصفحة
    if (!isSubPage) {
      item.innerHTML = `
        <img src="${posterUrl}" alt="${movie.title}" class="search-thumb">
        <span>${movie.title}</span>
      `;
    } else {
      item.innerHTML = `<span>${movie.title}</span>`;
    }

    item.onclick = () => {
      location.href = movieUrl;
    };

    resultBox.appendChild(item);
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
