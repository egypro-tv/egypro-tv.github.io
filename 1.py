import os
import json
import requests

# ============================
# إعدادات
# ============================
BASE_DIR = r"C:\Users\online\Desktop\Desktop\egypro\series"  # مجلد ملفات json لكل مسلسل
OUTPUT_DIR = BASE_DIR  # نفس المكان
SERIES_AR_PAGE = r"C:\Users\online\Desktop\Desktop\egypro\seriesen.html"

TMDB_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZjY0OWM4M2FjMDUwNTlkYjU0Y2UwM2Q1NTVmMmNkNCIsIm5iZiI6MTc1OTgyNDc2NS4xODIwMDAyLCJzdWIiOiI2OGU0Y2I3ZDc2MDQwMDUyYTljMjJlYmMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.D82HC8YMDOuqq89GLdGeMXdjPLCgIn8fTrBz8QmMF-0"
HEADERS = {
    "accept": "application/json",
    "Authorization": TMDB_TOKEN
}

# ============================
# دوال TMDB
# ============================

def search_series(title):
    url = "https://api.themoviedb.org/3/search/tv"
    r = requests.get(url, headers=HEADERS, params={"query": title}).json()
    if not r.get("results"):
        return None
    return r["results"][0]["id"]

def get_series_details(series_id):
    url = f"https://api.themoviedb.org/3/tv/{series_id}"
    ar = requests.get(url, headers=HEADERS, params={"language": "ar-AE"}).json()
    en = requests.get(url, headers=HEADERS, params={"language": "ar-AE"}).json()
    return ar, en

def get_series_credits(series_id):
    url = f"https://api.themoviedb.org/3/tv/{series_id}/credits"
    return requests.get(url, headers=HEADERS).json()

# ============================
# HTML القالب
# ============================

def build_episode_page(name, year, overview, poster, backdrop, cast_html,
                       director, producer, status, popularity, trailer,
                       ep_num, watch, download, ep_buttons, rating="N/A"):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{name} - الحلقة {ep_num} - EGY PRO</title>
<link href="../../style.css" rel="stylesheet"/>
<link href="../favicon.ico" rel="icon" type="image/x-icon"/>
</head>
<body>

<header class="site-header">
<nav class="nav-links">
<a href="../../index.html">الصفحه الرئيسيه</a>
<a href="../../egyptian.html">افلام عربية</a>
<a href="../../foreign.html">أفلام أجنبي</a>
<a href="../../seriesar.html">مسلسلات عربية</a>
<a href="../../seriesen.html">مسلسلات اجنبي</a>
<a href="../../anime.html">انمي</a>
<a href="../../live.html" class="active-link">بث مباشر كورة</a>
</nav>
</header>


<div class="search-bar">
  <input type="text" id="searchInput" placeholder="ابحث عن فيلم أو مسلسل..." />
  <button id="searchBtn">بحث</button>
  <div id="searchResults" class="search-results"></div>
</div>




<main>
<section class="movie-hero" style="background-image: url('{backdrop}');">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <div class="poster-col">
        <img alt="{name}" class="big-poster" src="{poster}"/>
      </div>
      <div class="info-col">
        <h1 class="movie-title"> {name} - الحلقة {ep_num} <span class="year">({year})</span></h1>
        <div class="meta">
          <span>⭐ {rating}</span>
          <span>مناسب للعائلة</span>
        </div>
        <p class="overview"><strong>الوصف:</strong> {overview}</p>
        <div class="actions">
          <a class="btn" href="{trailer}" rel="noopener" target="_blank">مشاهدة الإعلان</a>
          <a class="btn2" href="#watch-section">مشاهدة و تحميل المسلسل</a>
        </div>
        <div class="credits-section">
          <h4>الممثلون</h4>
          <ul>
            {cast_html}
          </ul>
          <div class="crew-info">
            <p><strong>المخرج:</strong> {director}</p>
            <p><strong>المنتج:</strong> {producer}</p>
          </div>
        </div>
        <div class="extra">
          <p><strong>اللغة:</strong> العربية</p>
          <p><strong>شركة الإنتاج:</strong> {producer}</p>
          <p><strong>الحالة:</strong> {status}</p>
          <p><strong>الأصلية:</strong> {name}</p>
          <p><strong>الشعبية:</strong> {popularity}</p>
        </div>
      </div>
    </div>
  </section>
</main>

<div class="episodes-container">
{ep_buttons}
</div>

<section class="watch-section" id="watch-section">
<h2 class="watch-title">مشاهدة الحلقة {ep_num}</h2>



<div class="video-player">
<iframe allowfullscreen frameborder="0" src="{watch}"></iframe>
</div>
<div class="download-buttons">
<a href="{download}" class="btn2" target="_blank">تحميل</a>
</div>
</section>

</body>
</html>'''

# ============================
# تشغيل
# ============================

for file in os.listdir(BASE_DIR):
    if not file.endswith(".json"):
        continue

    path = os.path.join(BASE_DIR, file)
    with open(path, "r", encoding="utf-8") as f:
        episodes = json.load(f)

    if not episodes:
        continue

    title = episodes[0]["title"]
    print("\n🔎", title)

    series_id = search_series(title)
    if not series_id:
        print("❌ لم يتم العثور عليه في TMDB")
        continue

    ar, en = get_series_details(series_id)
    credits = get_series_credits(series_id)

    name = ar.get("name") or en.get("name")
    overview = ar.get("overview") or en.get("overview")
    year = (en.get("first_air_date") or "0000")[:4]

    poster_path = en.get("poster_path")
    backdrop_path = en.get("backdrop_path")

    folder = os.path.join(OUTPUT_DIR, name.replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    # تحميل الصور
    poster = "poster.jpg"
    backdrop = "backdrop.jpg"
    if poster_path:
        img = requests.get(f"https://image.tmdb.org/t/p/w500{poster_path}").content
        open(os.path.join(folder, poster), "wb").write(img)

    if backdrop_path:
        img = requests.get(f"https://image.tmdb.org/t/p/w1280{backdrop_path}").content
        open(os.path.join(folder, backdrop), "wb").write(img)

    # cast
    cast_html = ""
    for p in credits.get("cast", [])[:10]:
        cast_html += f"<li>{p['name']}</li>\n"

    director = "غير متوفر"
    producer = "غير متوفر"
    for c in credits.get("crew", []):
        if c["job"] == "Director": director = c["name"]
        if c["job"] == "Producer": producer = c["name"]

    # rating، status، popularity
    rating = en.get("vote_average", "N/A")
    status = en.get("status", "غير معروف")
    popularity = en.get("popularity", "0")

    # التريلر
    videos = requests.get(
        f"https://api.themoviedb.org/3/tv/{series_id}/videos",
        headers=HEADERS,
        params={"language": "en-US"}
    ).json()

    trailer = "#"
    for v in videos.get("results", []):
        if v["type"] == "Trailer" and v["site"] == "YouTube":
            trailer = f"https://www.youtube.com/watch?v={v['key']}"
            break

    # ترتيب الحلقات
    episodes = sorted(episodes, key=lambda x: int(x["ep"]))

    # أزرار الحلقات
    ep_buttons = ""
    for ep in episodes:
        n = int(ep["ep"])
        ep_buttons += f'<button class="btn3" onclick="location.href=\'{n}.html\'">حلقة {n}</button>\n'

    # إنشاء صفحات لكل حلقة
    for ep in episodes:
        n = int(ep["ep"])
        code = ep["filecode"]
        watch = f"https://dood.to/e/{code}"
        download = f"https://dood.to/d/{code}"

        html = build_episode_page(
            name, year, overview, poster, backdrop, cast_html,
            director, producer, status, popularity, trailer,
            n, watch, download, ep_buttons, rating
        )

        with open(os.path.join(folder, f"{n}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    print("✅ تم إنشاء صفحات المسلسل")
    # ============================
    # إضافة كارت المسلسل في seriesar.html
    # ============================
    with open(SERIES_AR_PAGE, "r", encoding="utf-8") as f:
        series_page_html = f.read()

    # إنشاء كارت المسلسل
    series_card = f'''
    <div class="movie-card" onclick="location.href='series/{name.replace(" ", "_")}/1.html'">
        <img alt="{name}" src="series/{name.replace(" ", "_")}/{poster}" loading="lazy"/>
        <div class="movie-info">
            <h3 title="{name}">{name} {year}</h3>
            <p style="display: flex; align-items: center; gap: 4px; margin:0;">
                <img alt="star" src="1.ico" style="width:16px; height:16px;"/>
                <span>{rating} • {year}</span>
            </p>
        </div>
    </div>
    '''

    # إضافة الكارت داخل section.movie-grid
    split_marker = '<section class="movie-grid" id="movie-grid">'
    parts = series_page_html.split(split_marker)
    new_series_page_html = parts[0] + split_marker + '\n' + series_card + parts[1]

    # حفظ الصفحة بعد إضافة الكارت
    with open(SERIES_AR_PAGE, "w", encoding="utf-8") as f:
        f.write(new_series_page_html)


print("\n🏁 انتهى الكل")
