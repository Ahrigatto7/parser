from hanspell import spell_checker
import re

def correct_text_korean(text):
    sentences = re.split(r'(?<=[.!?。?!])\s+', text.strip())
    corrected = []
    for sent in sentences:
        try:
            result = spell_checker.check(sent)
            corrected.append(result.checked)
        except Exception:
            corrected.append(sent)
    return "\n".join(corrected)

# 바탕화면 경로에 맞춰 수정
input_path = r"C:\Users\oo\Desktop\Book1.txt"
output_path = r"C:\Users\oo\Desktop\Book1_교정본.txt"

# 텍스트 불러오기
with open(input_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# 교정 수행
corrected_text = correct_text_korean(raw_text)

# 결과 저장
with open(output_path, "w", encoding="utf-8") as file:
    file.write(corrected_text)

print("✅ 교정 완료! → 바탕화면에 Book1_교정본.txt 생성됨")
