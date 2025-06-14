"""Small demo for ontology utilities."""
from ontology import relation_of, get_definition

if __name__ == "__main__":
    dm = "목"
    others = ["화", "토", "금", "수", "목"]
    print("일간:", dm)
    for o in others:
        rel = relation_of(dm, o)
        desc = get_definition(rel) or "정의 없음"
        print(f"  {o} => {rel} ({desc})")

