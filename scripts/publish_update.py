from __future__ import annotations

import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = ROOT / "updates"
INDEX = UPDATES / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

TITLE = os.getenv("UPDATE_TITLE", "").strip()
CATEGORY = os.getenv("UPDATE_CATEGORY", "Обновление").strip() or "Обновление"
SUMMARY = os.getenv("UPDATE_SUMMARY", "").strip()
DETAILS = os.getenv("UPDATE_DETAILS", "").strip()
AUDIENCE = os.getenv("UPDATE_AUDIENCE", "").strip()
PRODUCT_LINK = os.getenv("UPDATE_PRODUCT_LINK", "https://calcul369.ru").strip() or "https://calcul369.ru"

if not TITLE or not SUMMARY:
    print("UPDATE_TITLE and UPDATE_SUMMARY are required.", file=sys.stderr)
    sys.exit(2)

combined = "\n".join([TITLE, CATEGORY, SUMMARY, DETAILS, AUDIENCE, PRODUCT_LINK])

secret_patterns = [
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._-]{15,}",
    r"(?i)(?:password|passwd|secret|token)\s*[=:]\s*[^\s]{8,}",
]
for pattern in secret_patterns:
    if re.search(pattern, combined):
        print("Publication stopped: possible secret detected.", file=sys.stderr)
        sys.exit(3)

translit = str.maketrans({
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"e","ж":"zh","з":"z",
    "и":"i","й":"y","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r",
    "с":"s","т":"t","у":"u","ф":"f","х":"h","ц":"c","ч":"ch","ш":"sh","щ":"sch",
    "ы":"y","э":"e","ю":"yu","я":"ya","ь":"","ъ":"",
})

def slugify(value: str) -> str:
    value = value.lower().translate(translit)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:80] or "update"

today = datetime.now(timezone.utc).date().isoformat()
UPDATES.mkdir(parents=True, exist_ok=True)
base = UPDATES / f"{today}-{slugify(TITLE)}.md"
page = base
counter = 2
while page.exists():
    page = UPDATES / f"{today}-{slugify(TITLE)}-{counter}.md"
    counter += 1

details_section = DETAILS or SUMMARY
audience_section = AUDIENCE or "Пользователи БАЗИС"

page_content = f"""# {TITLE}

**Категория:** {CATEGORY}  
**Дата:** {today}

## Кратко

{SUMMARY}

## Что изменилось

{details_section}

## Для кого

{audience_section}

## Перейти в БАЗИС

[{PRODUCT_LINK}]({PRODUCT_LINK})

---

[← Все обновления](README.md)
"""
page.write_text(page_content, encoding="utf-8")

relative = page.relative_to(ROOT).as_posix()
entry = f"- **{today} — [{TITLE}]({page.name})** — {SUMMARY}"

index_text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else "# Обновления БАЗИС\n\n<!-- AUTO-UPDATE-INDEX:START -->\n<!-- AUTO-UPDATE-INDEX:END -->\n"
start = "<!-- AUTO-UPDATE-INDEX:START -->"
end = "<!-- AUTO-UPDATE-INDEX:END -->"
if start not in index_text or end not in index_text:
    index_text += f"\n{start}\n{end}\n"
before, rest = index_text.split(start, 1)
current, after = rest.split(end, 1)
current = current.strip()
if current == "Пока автоматических публикаций нет.":
    current = ""
new_current = entry + ("\n" + current if current else "")
INDEX.write_text(f"{before}{start}\n{new_current}\n{end}{after}", encoding="utf-8")

changelog = CHANGELOG.read_text(encoding="utf-8")
cstart = "<!-- AUTO-PUBLIC-UPDATES:START -->"
cend = "<!-- AUTO-PUBLIC-UPDATES:END -->"
if cstart not in changelog or cend not in changelog:
    marker_block = f"\n## Автоматические публичные обновления\n\n{cstart}\n{cend}\n"
    insert_at = changelog.find("\n## ")
    if insert_at == -1:
        changelog += marker_block
    else:
        changelog = changelog[:insert_at] + marker_block + changelog[insert_at:]

before, rest = changelog.split(cstart, 1)
current, after = rest.split(cend, 1)
current = current.strip()
changelog_entry = f"### {today} — {TITLE}\n\n{SUMMARY}\n\n[Подробнее]({relative})"
new_current = changelog_entry + ("\n\n" + current if current else "")
CHANGELOG.write_text(f"{before}{cstart}\n{new_current}\n{cend}{after}", encoding="utf-8")

print(f"Created {relative}")
