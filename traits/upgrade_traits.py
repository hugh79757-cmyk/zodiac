import os
import re

# ==========================================
# 📂 설정: 성격 페이지 폴더
# ==========================================
TARGET_FOLDER = "./traits" 

# ==========================================
# 1. 삽입할 HTML (국기 버튼)
# ==========================================
FLAG_HTML = """
    <!-- 🌍 국기 버튼 (자동 삽입됨) -->
    <div class="translation-flags">
        <a href="javascript:void(0)" onclick="triggerTranslate('ko')" class="flag-btn" title="한국어"><img src="https://flagcdn.com/w80/kr.png" alt="KR"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('en')" class="flag-btn" title="English"><img src="https://flagcdn.com/w80/us.png" alt="US"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('zh-CN')" class="flag-btn" title="中文"><img src="https://flagcdn.com/w80/cn.png" alt="CN"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('ja')" class="flag-btn" title="日本語"><img src="https://flagcdn.com/w80/jp.png" alt="JP"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('th')" class="flag-btn" title="ไทย"><img src="https://flagcdn.com/w80/th.png" alt="TH"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('vi')" class="flag-btn" title="Tiếng Việt"><img src="https://flagcdn.com/w80/vn.png" alt="VN"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('id')" class="flag-btn" title="Indonesia"><img src="https://flagcdn.com/w80/id.png" alt="ID"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('es')" class="flag-btn" title="Español"><img src="https://flagcdn.com/w80/es.png" alt="ES"></a>
        <a href="javascript:void(0)" onclick="triggerTranslate('fr')" class="flag-btn" title="Français"><img src="https://flagcdn.com/w80/fr.png" alt="FR"></a>
    </div>
    <div id="google_translate_element" style="display:none;"></div>
"""

# ==========================================
# 2. 삽입할 CSS (국기 보이게 하기 + 이미지 수정)
# ==========================================
CSS_CODE = """
    <style>
        /* 🌍 국기 버튼 스타일 */
        .translation-flags {
            display: flex; justify-content: center; gap: 10px;
            padding: 15px 0; flex-wrap: wrap; 
            background: #fff; /* 배경색 추가해서 잘 보이게 */
            position: relative; z-index: 10001;
            border-bottom: 1px solid #eee;
        }
        .flag-btn {
            display: block; width: 34px; height: 34px; border-radius: 50%; overflow: hidden;
            border: 2px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.2s; cursor: pointer; background: white;
        }
        .flag-btn img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.1); }
        .flag-btn:hover { transform: translateY(-3px); border-color: #D4A84B; }

        /* 🖼️ 프로필 이미지 스타일 수정 (깨짐 방지) */
        .profile-img {
            width: 100px; height: 100px; 
            border-radius: 50%; 
            border: 4px solid rgba(255,255,255,0.9); 
            background: white; 
            object-fit: cover; /* contain에서 cover로 변경 */
            margin-bottom: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        /* 🚫 구글 번역 상단 바 강제 제거 */
        body { top: 0 !important; position: static !important; min-height: 100vh !important; }
        .goog-te-banner-frame { display: none !important; height: 0 !important; visibility: hidden !important; }
    </style>
"""

# ==========================================
# 3. 삽입할 JS (번역 기능)
# ==========================================
JS_CODE = """
    <script>
    function googleTranslateElementInit() {
        new google.translate.TranslateElement({
            pageLanguage: 'ko',
            includedLanguages: 'ko,en,zh-CN,ja,th,vi,id,es,fr',
            autoDisplay: false
        }, 'google_translate_element');
        setTimeout(function() {
            const savedLang = localStorage.getItem('selectedLang');
            if (savedLang && savedLang !== 'ko') { triggerTranslate(savedLang); }
        }, 500);
    }
    function triggerTranslate(langCode) {
        const select = document.querySelector('.goog-te-combo');
        if (select) {
            select.value = langCode;
            select.dispatchEvent(new Event('change'));
            localStorage.setItem('selectedLang', langCode);
        }
    }
    (function() {
        var gtScript = document.createElement('script');
        gtScript.type = 'text/javascript'; gtScript.async = true;
        gtScript.src = "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
        document.body.appendChild(gtScript);
    })();
    </script>
"""

def fix_traits_pages():
    count = 0
    if not os.path.exists(TARGET_FOLDER):
        print(f"❌ 오류: '{TARGET_FOLDER}' 폴더를 찾을 수 없습니다.")
        return

    for filename in os.listdir(TARGET_FOLDER):
        if filename.endswith(".html"):
            file_path = os.path.join(TARGET_FOLDER, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ----------------------------------------------------
            # 1. 기존에 잘못 들어간 국기 코드 삭제 (청소)
            # ----------------------------------------------------
            # 정규식으로 <div class="translation-flags">...</div> 덩어리 제거
            content = re.sub(r'<div class="translation-flags">.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div id="google_translate_element".*?></div>', '', content)

            # ----------------------------------------------------
            # 2. 올바른 위치에 국기 버튼 삽입
            # ----------------------------------------------------
            # <body> 태그 바로 뒤에 넣습니다.
            if "<body" in content:
                body_idx = content.find(">", content.find("<body")) + 1
                content = content[:body_idx] + "\n" + FLAG_HTML + content[body_idx:]

            # ----------------------------------------------------
            # 3. 이미지 경로 수정 (상대경로 -> 절대경로)
            # ----------------------------------------------------
            # src="rat.png" 처럼 되어있는 것을 src="/images/zodiac/rat.png" 로 변경
            # (이미 /images/ 로 되어있으면 건드리지 않음)
            
            # 정규식: src="...png" 에서 경로가 없는 파일명만 잡음
            def replace_img_path(match):
                img_name = match.group(1)
                # 이미 경로가 있으면 그대로 둠
                if '/' in img_name: return f'src="{img_name}"'
                return f'src="/images/zodiac/{img_name}"'

            content = re.sub(r'src="([^"]+\.png)"', replace_img_path, content)

            # ----------------------------------------------------
            # 4. CSS 및 JS 주입
            # ----------------------------------------------------
            # 기존 CSS/JS가 있으면 교체하기 복잡하므로, </head>와 </body> 앞에 새로 추가
            # (CSS는 나중에 나온게 덮어쓰므로 OK)
            
            if "/* 🌍 국기 버튼 스타일 */" not in content:
                content = content.replace("</head>", CSS_CODE + "\n</head>")
            
            if "googleTranslateElementInit" not in content:
                content = content.replace("</body>", JS_CODE + "\n</body>")

            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 복구 완료: {filename}")
            count += 1

    print(f"\n🎉 총 {count}개 성격 페이지 복구 완료!")

if __name__ == "__main__":
    fix_traits_pages()
