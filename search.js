let movies = [];
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultBox = document.getElementById('searchResults');

// 📥 تحميل ملف الأفلام
async function loadMovies() {
  const paths = ['../../movies.json'];
  for (const path of paths) {
    try {
      const response = await fetch(path);
      if (response.ok) {
        movies = await response.json();
        console.log('✅ تم تحميل البيانات من:', path);
        return;
      }
    } catch (e) {
      // تجاهل الخطأ وجرب المسار التالي
    }
  }
  console.error('❌ لم يتم العثور على movies.json في أي مسار');
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
  const filtered = movies.filter(movie =>
    searchWords.some(word => movie.title.toLowerCase().includes(word))
  );

  if (filtered.length === 0) {
    resultBox.style.display = 'block';
    resultBox.innerHTML = `<p class="no-results">لا توجد نتائج</p>`;
    return;
  }

  resultBox.style.display = 'block';

  // 🔍 هل الصفحة فرعية؟
  const isSubPage = window.location.pathname.split('/').length > 3;

  filtered.forEach(movie => {
    const item = document.createElement('div');
    item.classList.add('search-item');

    const movieUrl = movie.url.startsWith('/') ? movie.url : '/' + movie.url;

    // ✅ لو الصفحة الرئيسية: عرض الصورة + الاسم
    // ✅ لو صفحة فرعية: عرض الاسم فقط
    if (!isSubPage) {
      item.innerHTML = `
        <img src="${movie.poster}" alt="${movie.title}" class="search-thumb">
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

searchBtn.addEventListener('click', searchMovies);
searchInput.addEventListener('keyup', searchMovies);

// 🔹 إخفاء القائمة عند الضغط خارج مربع البحث
document.addEventListener('click', (e) => {
  if (!e.target.closest('.search-bar')) {
    resultBox.style.display = 'none';
  }
});
