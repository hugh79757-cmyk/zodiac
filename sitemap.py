import os
import datetime

# ==========================================
# 🌍 사이트 도메인 설정
# ==========================================
BASE_URL = "https://zodiac.techpawz.com"
TODAY = datetime.date.today().isoformat()

def generate_sitemap():
    print("사이트맵 생성을 시작합니다...")
    
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # 1. 메인 페이지 (index.html)
    print(" - 메인 페이지 추가 중...")
    xml_content.append(f"""    <url>
        <loc>{BASE_URL}/</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>""")

    # 2. 궁합 페이지 (posts 폴더 - 432개)
    if os.path.exists("./posts"):
        posts_count = 0
        for filename in os.listdir("./posts"):
            if filename.endswith(".html"):
                xml_content.append(f"""    <url>
        <loc>{BASE_URL}/posts/{filename}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
                posts_count += 1
        print(f" - 궁합 페이지 {posts_count}개 추가 완료")
    else:
        print("⚠️ 경고: './posts' 폴더를 찾을 수 없습니다.")

    # 3. 성격 페이지 (traits 폴더 - 24개)
    if os.path.exists("./traits"):
        traits_count = 0
        for filename in os.listdir("./traits"):
            if filename.endswith(".html"):
                xml_content.append(f"""    <url>
        <loc>{BASE_URL}/traits/{filename}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
                traits_count += 1
        print(f" - 성격 페이지 {traits_count}개 추가 완료")
    else:
        print("⚠️ 경고: './traits' 폴더를 찾을 수 없습니다.")

    xml_content.append('</urlset>')

    # 파일 저장
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))

    print("\n✅ sitemap.xml 파일이 성공적으로 생성되었습니다!")

if __name__ == "__main__":
    generate_sitemap()
