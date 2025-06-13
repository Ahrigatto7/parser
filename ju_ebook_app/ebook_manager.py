
import json
from typing import List, Dict

class EbookManager:
    def __init__(self, path: str = None):
        self.ebook_data: Dict[str, Dict] = {}
        self.path = path
        if path:
            self.load(path)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.ebook_data = json.load(f)
        self.path = path

    def save(self, path: str = None):
        if not path:
            path = self.path
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.ebook_data, f, ensure_ascii=False, indent=2)

    def add_concept(self, concept: str, definition: str = ""):
        if concept not in self.ebook_data:
            self.ebook_data[concept] = {"정의": definition, "사례": []}
        elif definition:
            self.ebook_data[concept]["정의"] = definition

    def add_case(self, concept: str, saju: str, description: str):
        if concept not in self.ebook_data:
            self.add_concept(concept)
        self.ebook_data[concept]["사례"].append({
            "사주": saju,
            "설명": description
        })

    def get_concept(self, concept: str) -> Dict:
        return self.ebook_data.get(concept, {})

    def list_concepts(self) -> List[str]:
        return list(self.ebook_data.keys())

    def concept_exists(self, concept: str) -> bool:
        return concept in self.ebook_data
