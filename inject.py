import os

# المسار الأساسي
base_path = r"C:\Users\online\Desktop\Desktop\egypro\agnby"

# الكود اللي هيتضاف
ad_code = """
<script>
(function(olag){
var d = document,
    s = d.createElement('script'),
    l = d.scripts[d.scripts.length - 1];
s.settings = olag || {};
s.src = "\/\/insistentbonus.com\/b.XaVZsIdiGKlX0XYGWrcg\/te_mb9FuvZ\/UnlwkJPXTTYM4oMDDCAywEMEz-cbtUNhj\/g_waMXD\/A\/0QMOQh";
s.async = true;
s.referrerPolicy = 'no-referrer-when-downgrade';
l.parentNode.insertBefore(s, l);
})({})
</script>
"""

# عداد الملفات المعدلة
count = 0

# لف على كل الفولدرات والملفات
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.lower().endswith(".html"):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # لو الكود مش موجود بالفعل
                if ad_code.strip() not in content and "<main" in content.lower():
                    
                    # البحث عن <main> (case insensitive)
                    index = content.lower().find("<main")
                    
                    new_content = content[:index] + ad_code + "\n" + content[index:]

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

                    count += 1
                    print(f"✔ تم التعديل: {file_path}")

            except Exception as e:
                print(f"❌ خطأ في الملف: {file_path}")
                print(e)

print(f"\n🎉 تم تعديل {count} ملف بنجاح")
