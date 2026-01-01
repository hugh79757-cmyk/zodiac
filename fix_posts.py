import os
import re

# posts 폴더 경로
POSTS_DIR = "./posts"

# 새로운 통일된 CSS (구글 번역 바 공간 확보)
NEW_CSS = '''
    <style>
        /* 🌍 국기 버튼 스타일 */
        .translation-flags {
            display: flex; 
            justify-content: center; 
            gap: 12px;
            padding: 20px 0 10px; 
            margin-top: 50px;  /* 구글 번역 바 공간 확보 */
            flex-wrap: wrap; 
            position: relative; 
            z-index: 10001;
            background-color: #fdf8f0;
        }

        .flag-btn {
            display: block; 
            width: 36px; 
            height: 36px; 
            border-radius: 50%; 
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.6); 
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            transition: all 0.2s; 
            cursor: pointer; 
            background: white;
        }

        .flag-btn img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            transform: scale(1.1); 
        }

        .flag-btn:hover { 
            transform: translateY(-3px) scale(1.15); 
            border-color: #D4A84B; 
        }

        /* 🚫 구글 번역 상단 바 - 위치는 유지하되 body 밀림 방지 */
        body { 
            top: 0 !important; 
            position: static !important; 
            min-height: 100vh !important; 
        }

        /* 번역 바가 있을 때 추가 여백 */
        body.translated-ltr .translation-flags,
        body.translated-rtl .translation-flags {
            margin-top: 50px;
        }

        .goog-tooltip { 
            display: none !important; 
        }

        .goog-text-highlight { 
            background-color: transparent !important; 
            box-shadow: none !important; 
        }

        /* 모바일 최적화 */
        @media (max-width: 480px) {
            .translation-flags {
                justify-content: flex-start; 
                overflow-x: auto;
                padding-left: 20px; 
                padding-right: 20px; 
                white-space: nowrap; 
                flex-wrap: nowrap;
                scrollbar-width: none;
            }
            .translation-flags::-webkit-scrollbar { 
                display: none; 
            }
            .flag-btn { 
                flex: 0 0 auto; 
            }
        }
    </style>
'''

# 새로운 통일된 HTML (국기 버튼)
NEW_FLAGS_HTML = '''
<!-- 🌍 국기 버튼 -->
<div class="translation-flags">
    <a href="javascript:void(0)" onclick="triggerTranslate('ko')" class="flag-btn" title="한국어"><img src="https://flagcdn.com/w80/kr.png" alt="KR"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('en')" class="flag-btn" title="English"><img src="https://flagcdn.com/w80/gb.png" alt="UK"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('zh-CN')" class="flag-btn" title="中文"><img src="https://flagcdn.com/w80/cn.png" alt="CN"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('ja')" class="flag-btn" title="日本語"><img src="https://flagcdn.com/w80/jp.png" alt="JP"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('th')" class="flag-btn" title="ไทย"><img src="https://flagcdn.com/w80/th.png" alt="TH"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('vi')" class="flag-btn" title="Tiếng Việt"><img src="https://flagcdn.com/w80/vn.png" alt="VN"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('id')" class="flag-btn" title="Indonesia"><img src="https://flagcdn.com/w80/id.png" alt="ID"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('es')" class="flag-btn" title="Español"><img src="https://flagcdn.com/w80/es.png" alt="ES"></a>
    <a href="javascript:void(0)" onclick="triggerTranslate('fr')" class="flag-btn" title="Français"><img src="https://flagcdn.com/w80/fr.png" alt="FR"></a>
</div>
<div id="google_translate_element" style="display:none;"></div>
'''

def fix_file(filepath):
    """파일 하나를 수정하는 함수"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 기존 translation-flags 관련 모든 <style> 블록 제거
        # 패턴: <style> 안에 .translation-flags 또는 .flag-btn이 있는 경우
        def remove_flag_styles(match):
            style_content = match.group(0)
            if '.translation-flags' in style_content or '.flag-btn' in style_content or 'goog-te-banner' in style_content:
                return ''
            return style_content
        
        content = re.sub(r'<style>.*?</style>', remove_flag_styles, content, flags=re.DOTALL)
        
        # 2. 기존 국기 버튼 HTML 모두 제거
        # 패턴 1: 주석 포함된 버전
        content = re.sub(
            r'<!--\s*🌍.*?-->\s*<div class="translation-flags"[^>]*>.*?</div>\s*<div id="google_translate_element"[^>]*></div>',
            '{{FLAGS_PLACEHOLDER}}',
            content,
            flags=re.DOTALL
        )
        
        # 패턴 2: 주석 없는 버전  
        content = re.sub(
            r'<div class="translation-flags"[^>]*>.*?</div>\s*<div id="google_translate_element"[^>]*></div>',
            '{{FLAGS_PLACEHOLDER}}',
            content,
            flags=re.DOTALL
        )
        
        # 3. 중복 플레이스홀더 제거 (하나만 남김)
        placeholder_count = content.count('{{FLAGS_PLACEHOLDER}}')
        if placeholder_count > 1:
            content = content.replace('{{FLAGS_PLACEHOLDER}}', '', placeholder_count - 1)
        
        # 4. 플레이스홀더가 없으면 <body> 바로 뒤에 추가
        if '{{FLAGS_PLACEHOLDER}}' not in content:
            content = re.sub(
                r'(<body[^>]*>)',
                r'\1\n{{FLAGS_PLACEHOLDER}}',
                content
            )
        
        # 5. 플레이스홀더를 새로운 HTML로 교체
        content = content.replace('{{FLAGS_PLACEHOLDER}}', NEW_FLAGS_HTML)
        
        # 6. </head> 앞에 새로운 CSS 추가
        if 'margin-top: 50px' not in content:
            content = re.sub(
                r'(</head>)',
                NEW_CSS + r'\n\1',
                content
            )
        
        # 7. 빈 줄 정리
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"❌ 오류 발생: {filepath} - {e}")
        return False

def main():
    """메인 함수"""
    if not os.path.exists(POSTS_DIR):
        print(f"❌ '{POSTS_DIR}' 폴더를 찾을 수 없습니다.")
        print("zodiac 프로젝트 루트 폴더에서 실행해주세요.")
        return
    
    html_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.html')]
    
    print(f"📁 {len(html_files)}개의 HTML 파일을 발견했습니다.")
    print("=" * 50)
    
    modified_count = 0
    
    for filename in html_files:
        filepath = os.path.join(POSTS_DIR, filename)
        if fix_file(filepath):
            print(f"✅ 수정 완료: {filename}")
            modified_count += 1
        else:
            print(f"⏭️  변경 없음: {filename}")
    
    print("=" * 50)
    print(f"🎉 완료! {modified_count}개 파일이 수정되었습니다.")

if __name__ == "__main__":
    main()
