
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QFileDialog, QMessageBox
)
from ebook_manager import EbookManager
import re
from saju_parser import parse_saju_structure
import csv

class EbookTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = EbookManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.concept_input = QLineEdit()
        self.definition_input = QTextEdit()
        self.saju_input = QLineEdit()
        self.description_input = QTextEdit()
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        add_concept_btn = QPushButton("📌 개념 추가")
        add_case_btn = QPushButton("➕ 사례 추가")
        view_btn = QPushButton("🔍 개념 보기")
        save_btn = QPushButton("💾 저장")
        load_btn = QPushButton("📂 불러오기")
        parse_btn = QPushButton("📁 문서 분석")
        csv_btn = QPushButton("📥 개념 CSV 불러오기")  # 정의 순서 수정

        add_concept_btn.clicked.connect(self.add_concept)
        add_case_btn.clicked.connect(self.add_case)
        view_btn.clicked.connect(self.view_concept)
        save_btn.clicked.connect(self.save_ebook)
        load_btn.clicked.connect(self.load_ebook)
        parse_btn.clicked.connect(self.parse_document)
        csv_btn.clicked.connect(self.load_concepts_from_csv)

        layout.addWidget(QLabel("개념 이름"))
        layout.addWidget(self.concept_input)
        layout.addWidget(QLabel("정의"))
        layout.addWidget(self.definition_input)
        layout.addWidget(add_concept_btn)

        layout.addWidget(QLabel("사주"))
        layout.addWidget(self.saju_input)
        layout.addWidget(QLabel("설명"))
        layout.addWidget(self.description_input)
        layout.addWidget(add_case_btn)

        layout.addWidget(view_btn)
        layout.addWidget(save_btn)
        layout.addWidget(load_btn)
        layout.addWidget(parse_btn)
        layout.addWidget(csv_btn)

        auto_parse_btn = QPushButton("📁 개념+사례 자동 분석")
        auto_parse_btn.clicked.connect(self.auto_parse_blocks)
        layout.addWidget(auto_parse_btn)


        layout.addWidget(QLabel("출력"))
        layout.addWidget(self.output)
        self.setLayout(layout)

    def add_concept(self):
        concept = self.concept_input.text().strip()
        definition = self.definition_input.toPlainText().strip()
        if concept:
            self.manager.add_concept(concept, definition)
            self.output.append(f"✅ 개념 '{concept}' 추가 또는 갱신됨.")
        else:
            QMessageBox.warning(self, "입력 오류", "개념 이름을 입력하세요.")

    def add_case(self):
        concept = self.concept_input.text().strip()
        saju = self.saju_input.text().strip()
        desc = self.description_input.toPlainText().strip()
        if concept and saju and desc:
            self.manager.add_case(concept, saju, desc)
            self.output.append(f"➕ 사례가 '{concept}' 개념에 추가됨.")
        else:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 채워주세요.")

    def save_ebook(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Ebook 저장", "", "JSON Files (*.json)")
        if fname:
            self.manager.save(fname)
            self.output.append(f"💾 저장됨: {fname}")

    def load_ebook(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Ebook 불러오기", "", "JSON Files (*.json)")
        if fname:
            self.manager.load(fname)
            self.output.append(f"📂 불러옴: {fname}")

    def view_concept(self):
        concept = self.concept_input.text().strip()
        if concept and self.manager.concept_exists(concept):
            data = self.manager.get_concept(concept)
            text = f"📘 {concept}\n정의: {data['정의']}\n사례 수: {len(data['사례'])}"
            for case in data["사례"]:
                text += f"\n\n• 사주: {case['사주']}\n  해석: {case['설명']}"
            self.output.setText(text)
        else:
            QMessageBox.warning(self, "개념 없음", f"'{concept}' 개념이 사전에 없습니다.")

    def parse_document(self):
        fname, _ = QFileDialog.getOpenFileName(self, "문서 선택", "", "Text Files (*.txt)")
        if not fname:
            return

        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()

        count = 0
        blocks = re.split(r"\n\s*\n", content)
        for block in blocks:
            lines = block.strip().splitlines()
            if len(lines) >= 2:
                concept = lines[0].strip()
                saju_line = lines[1]
                desc_line = " ".join(lines[2:]) if len(lines) > 2 else ""
                saju_match = re.search(r"[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥\s]{8,}", saju_line)
                if saju_match:
                    saju = saju_match.group(0).strip()
                    self.manager.add_concept(concept)
                    self.manager.add_case(concept, saju, desc_line)
                    self.output.append(f"📘 '{concept}' 개념 + ➕ 사례 추가됨")
                    count += 1

        if count == 0:
            self.output.append("⚠️ 인식 가능한 사례가 없습니다.")
        else:
            self.output.append(f"✅ 총 {count}건 자동 분석 및 등록됨.")

    def load_concepts_from_csv(self):
        fname, _ = QFileDialog.getOpenFileName(self, "개념 CSV 불러오기", "", "CSV Files (*.csv)")
        if not fname:
            return

        count = 0
        with open(fname, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                concept = row.get("개념", "").strip()
                definition = row.get("정의", "").strip()
                if concept:
                    self.manager.add_concept(concept, definition)
                    self.output.append(f"📘 '{concept}' 개념이 CSV에서 추가됨.")
                    count += 1

        self.output.append(f"✅ 총 {count}개 개념이 CSV에서 등록됨.")

    def auto_parse_blocks(self):
        fname, _ = QFileDialog.getOpenFileName(self, "자동 분석할 문서 선택", "", "Text Files (*.txt *.md)")
        if not fname:
            return

                # 예시: 사주 구조 분석 로그 출력 (1건이라도 있으면)
        if matches:
            try:
                parsed = parse_saju_structure(matches[0][1])
                self.output.append(f"🔍 일간: {parsed['천간']['일간']} / 성별: {parsed['성별']}")
            except Exception as e:
                self.output.append(f"⚠️ 사주 분석 오류: {str(e)}")

count = 0
        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()

        # 정규식 기반 블록 추출 (개념 + 사주 + 설명)
        pattern = re.compile(
            r"\[개념\]\s*(.*?)\s*사주[:：]?\s*([甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥\s]{8,})\s*설명[:：]?\s*(.*?)(?=\n\[개념\]|\Z)",
            re.DOTALL
        )
        matches = pattern.findall(content)

        for concept, saju, desc in matches:
            concept = concept.strip()
            saju = " ".join(saju.strip().split())
            desc = desc.strip().replace("\n", " ")
            if concept and saju:
                self.manager.add_concept(concept)
                self.manager.add_case(concept, saju, desc)
                self.output.append(f"📘 '{concept}' 개념 + ➕ 사례 등록됨")
                count += 1

        if count == 0:
            self.output.append("⚠️ 인식된 개념/사례가 없습니다. 포맷을 확인해주세요.")
        else:
            self.output.append(f"✅ 총 {count}건 자동 등록 완료.")
