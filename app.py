# -*- coding: utf-8 -*-
"""
🎓 ИнфоАссистент — информатика мұғалімдеріне арналған цифрлық көмекші
Іске қосу:  streamlit run app.py
Қосымша:  pip install openai   → ЖИ режимі үшін (Groq API)
"""

import ast
import builtins
import difflib
import html
import random
import os
import re
import textwrap

import streamlit as st

# ─────────────────────────────────────────────────────────────
# 1. БЕТ БАПТАУЛАРЫ ЖӘНЕ СТИЛЬ (CSS)
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ИнфоАссистент — мұғалімге арналған көмекші",
    page_icon="🎓",
    layout="wide",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --primary: #5B5BD6;
    --primary-dark: #3F3FB5;
    --accent: #FF8A65;
    --teal: #26A69A;
    --cream: #FFF8F1;
    --card: #FFFFFF;
    --text: #2B2D42;
    --muted: #6B6F85;
}

html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox {
    font-family: 'Nunito', sans-serif !important;
}

.stApp {
    background: linear-gradient(160deg, #FFF8F1 0%, #F3F1FF 55%, #E9FBF8 100%);
}

/* Бүйір панель */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4A4AC4 0%, #6C63FF 55%, #8E7CFF 100%);
}
section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
section[data-testid="stSidebar"] input { color: #2B2D42 !important; }

.brand {
    text-align: center;
    padding: 6px 0 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 14px;
}
.brand .logo { font-size: 46px; }
.brand .name { font-size: 22px; font-weight: 800; letter-spacing: .3px; }
.brand .slogan { font-size: 13px; opacity: .85; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #5B5BD6 0%, #8E7CFF 60%, #FF8A65 130%);
    color: white;
    padding: 42px 38px;
    border-radius: 26px;
    box-shadow: 0 14px 34px rgba(91,91,214,.28);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "🐍";
    position: absolute; right: 30px; bottom: -12px;
    font-size: 120px; opacity: .18;
}
.hero h1 { color: white; font-size: 38px; font-weight: 800; margin: 0 0 10px 0; }
.hero p  { font-size: 18px; line-height: 1.6; margin: 0; max-width: 760px; opacity: .96; }

/* Беттің тақырыбы */
.page-title {
    font-size: 32px; font-weight: 800; color: var(--primary-dark);
    margin-bottom: 4px;
}
.page-sub { color: var(--muted); font-size: 16px; margin-bottom: 22px; }

/* Карточкалар */
.feature {
    background: var(--card);
    border-radius: 22px;
    padding: 26px 22px;
    box-shadow: 0 8px 24px rgba(43,45,66,.08);
    border-top: 5px solid var(--primary);
    height: 100%;
    transition: transform .2s ease, box-shadow .2s ease;
}
.feature:hover { transform: translateY(-5px); box-shadow: 0 14px 30px rgba(43,45,66,.14); }
.feature.warm  { border-top-color: var(--accent); }
.feature.teal  { border-top-color: var(--teal); }
.feature .icon { font-size: 38px; margin-bottom: 6px; }
.feature h3 { margin: 4px 0 8px 0; color: var(--text); font-size: 20px; }
.feature p  { color: var(--muted); margin: 0; line-height: 1.55; font-size: 15px; }

.step {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 10px;
    box-shadow: 0 4px 14px rgba(43,45,66,.06);
    border-left: 6px solid var(--teal);
    color: var(--text);
    font-size: 16px;
}

.warm-note {
    background: #FFF1E6;
    border: 1px dashed var(--accent);
    color: #8A4B2A;
    padding: 16px 20px;
    border-radius: 18px;
    font-size: 16px;
    margin-top: 18px;
}

/* Тапсырма карталары */
.task-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 18px 22px 8px 22px;
    margin: 14px 0 6px 0;
    box-shadow: 0 6px 20px rgba(43,45,66,.08);
    border-left: 8px solid var(--primary);
}
.task-card.l1 { border-left-color: #66BB6A; }
.task-card.l2 { border-left-color: #FFB300; }
.task-card.l3 { border-left-color: #EF5350; }
.task-card h4 { margin: 6px 0 6px 0; color: var(--text); font-size: 18px; }
.task-card p  { color: var(--text); font-size: 16px; line-height: 1.6; }
.badge {
    display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 13px; font-weight: 700; color: white; background: var(--primary);
}
.badge.l1 { background: #66BB6A; }
.badge.l2 { background: #FFB300; }
.badge.l3 { background: #EF5350; }

/* Қателер */
.issue {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 16px 20px;
    margin: 10px 0;
    border-left: 7px solid var(--accent);
    box-shadow: 0 6px 18px rgba(43,45,66,.08);
}
.issue .where { font-weight: 800; color: #D84315; font-size: 15px; }
.issue .title { font-weight: 800; color: var(--text); font-size: 18px; margin: 2px 0 6px 0; }
.issue .why   { color: var(--text); font-size: 15.5px; line-height: 1.6; }

.diff-row {
    font-family: 'Courier New', monospace; font-size: 14px;
    border-radius: 10px; padding: 6px 12px; margin: 4px 0;
}
.diff-old { background: #FFEBEE; color: #B71C1C; }
.diff-new { background: #E8F5E9; color: #1B5E20; }

/* Батырмалар */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #5B5BD6, #8E7CFF);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 26px;
    font-size: 17px;
    font-weight: 800;
    box-shadow: 0 8px 18px rgba(91,91,214,.30);
    transition: all .2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #FF8A65, #FFA726);
    box-shadow: 0 10px 22px rgba(255,138,101,.38);
    color: white;
}

.stTextArea textarea {
    font-family: 'Courier New', monospace !important;
    border-radius: 14px !important;
    font-size: 15px !important;
}

.footer {
    text-align: center; color: var(--muted); font-size: 14px;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #E4E1F5;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 2. ТАПСЫРМАЛАР ДЕРЕКҚОРЫ (ДЕМО-РЕЖИМ)
# ─────────────────────────────────────────────────────────────

def C(code: str) -> str:
    return textwrap.dedent(code).strip("\n")


LEVELS = {
    "🌱 Базалық": "l1",
    "🌿 Орта": "l2",
    "🌳 Жоғары": "l3",
}

TOPICS = {
    "Сызықтық алгоритмдер": {
        "focus": "Енгізу, есептеу және шығару ретімен дұрыс құрылған",
        "levels": {
            "🌱 Базалық": [
                ("Пернетақтадан екі бүтін сан енгізіледі. Олардың қосындысын және көбейтіндісін шығаратын бағдарлама жазыңыз.",
                 C('''
                 a = int(input("Бірінші сан: "))
                 b = int(input("Екінші сан: "))
                 print("Қосынды:", a + b)
                 print("Көбейтінді:", a * b)
                 ''')),
                ("Тіктөртбұрыштың қабырғалары берілген. Оның периметрі мен ауданын табыңыз.",
                 C('''
                 a = float(input("Ұзындығы: "))
                 b = float(input("Ені: "))
                 print("Периметр:", 2 * (a + b))
                 print("Аудан:", a * b)
                 ''')),
            ],
            "🌿 Орта": [
                ("Уақыт секундпен берілген. Оны сағат, минут және секунд түрінде шығарыңыз.",
                 C('''
                 t = int(input("Секунд: "))
                 h = t // 3600
                 m = (t % 3600) // 60
                 s = t % 60
                 print(h, "сағ", m, "мин", s, "сек")
                 ''')),
                ("Екі таңбалы сан берілген. Оның цифрларының қосындысын және көбейтіндісін табыңыз.",
                 C('''
                 n = int(input("Екі таңбалы сан: "))
                 a = n // 10
                 b = n % 10
                 print("Қосынды:", a + b)
                 print("Көбейтінді:", a * b)
                 ''')),
            ],
            "🌳 Жоғары": [
                ("Үш таңбалы сан берілген. Оның цифрларын кері ретпен шығарыңыз (мысалы, 123 → 321). Тек // және % амалдарын қолданыңыз.",
                 C('''
                 n = int(input("Үш таңбалы сан: "))
                 a = n // 100
                 b = (n // 10) % 10
                 c = n % 10
                 print(c * 100 + b * 10 + a)
                 ''')),
                ("Екі айнымалының мәнін үшінші айнымалыны қолданбай ауыстырыңыз. Бұл әдіс неге жұмыс істейтінін түсіндіріңіз.",
                 C('''
                 a = int(input("a = "))
                 b = int(input("b = "))
                 a = a + b
                 b = a - b
                 a = a - b
                 print("a =", a, "b =", b)
                 ''')),
            ],
        },
    },
    "Шартты операторлар (if-else)": {
        "focus": "Шарттар дұрыс құрылған, барлық жағдай қамтылған",
        "levels": {
            "🌱 Базалық": [
                ("Сан енгізіледі. Оның оң, теріс немесе нөл екенін анықтаңыз.",
                 C('''
                 x = float(input("Сан: "))
                 if x > 0:
                     print("Оң сан")
                 elif x < 0:
                     print("Теріс сан")
                 else:
                     print("Нөл")
                 ''')),
                ("Оқушының жасы енгізіледі. Жасы 18-ден асса «Рұқсат етілген», әйтпесе «Рұқсат жоқ» деп шығарыңыз.",
                 C('''
                 age = int(input("Жасы: "))
                 if age >= 18:
                     print("Рұқсат етілген")
                 else:
                     print("Рұқсат жоқ")
                 ''')),
            ],
            "🌿 Орта": [
                ("Үш сан берілген. max() функциясын қолданбай, ең үлкенін табыңыз.",
                 C('''
                 a = int(input())
                 b = int(input())
                 c = int(input())
                 m = a
                 if b > m:
                     m = b
                 if c > m:
                     m = c
                 print("Ең үлкені:", m)
                 ''')),
                ("Жыл енгізіледі. Ол кібісе жыл ма, жоқ па — анықтаңыз.",
                 C('''
                 y = int(input("Жыл: "))
                 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
                     print("Кібісе жыл")
                 else:
                     print("Кібісе емес")
                 ''')),
            ],
            "🌳 Жоғары": [
                ("ax² + bx + c = 0 теңдеуінің түбірлерін табыңыз. a = 0 және дискриминант теріс болған жағдайларды ескеріңіз.",
                 C('''
                 import math
                 a = float(input("a: "))
                 b = float(input("b: "))
                 c = float(input("c: "))
                 if a == 0:
                     print("Бұл квадрат теңдеу емес")
                 else:
                     d = b ** 2 - 4 * a * c
                     if d > 0:
                         print("Түбірлері:", (-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a))
                     elif d == 0:
                         print("Бір түбір:", -b / (2 * a))
                     else:
                         print("Нақты түбір жоқ")
                 ''')),
                ("Оқушының балы (0–100) енгізіледі. Балға қарай бағаны (5, 4, 3, 2) шығарыңыз. Қате енгізуді тексеріңіз.",
                 C('''
                 ball = int(input("Балл (0-100): "))
                 if ball < 0 or ball > 100:
                     print("Қате: балл 0-ден 100-ге дейін болуы керек")
                 elif ball >= 85:
                     print("Баға: 5")
                 elif ball >= 65:
                     print("Баға: 4")
                 elif ball >= 40:
                     print("Баға: 3")
                 else:
                     print("Баға: 2")
                 ''')),
            ],
        },
    },
    "Циклдер (for, while)": {
        "focus": "Цикл түрі дұрыс таңдалған, шарт пен қадам қате емес",
        "levels": {
            "🌱 Базалық": [
                ("for циклі арқылы 1-ден 10-ға дейінгі сандарды шығарыңыз.",
                 C('''
                 for i in range(1, 11):
                     print(i)
                 ''')),
                ("while циклі арқылы 10-нан 1-ге дейін кері санаңыз.",
                 C('''
                 i = 10
                 while i >= 1:
                     print(i)
                     i -= 1
                 ''')),
            ],
            "🌿 Орта": [
                ("N саны берілген. 1-ден N-ге дейінгі сандардың қосындысын табыңыз.",
                 C('''
                 n = int(input("N = "))
                 s = 0
                 for i in range(1, n + 1):
                     s += i
                 print("Қосынды:", s)
                 ''')),
                ("Натурал сан берілген. while циклі арқылы оның неше цифрдан тұратынын анықтаңыз.",
                 C('''
                 n = int(input("Сан: "))
                 count = 0
                 while n > 0:
                     n //= 10
                     count += 1
                 print("Цифр саны:", count)
                 ''')),
            ],
            "🌳 Жоғары": [
                ("Сан жай сан ба, жоқ па — тексеріңіз. Циклді √n-ге дейін ғана жүргізіңіз.",
                 C('''
                 n = int(input("Сан: "))
                 is_prime = n > 1
                 i = 2
                 while i * i <= n:
                     if n % i == 0:
                         is_prime = False
                         break
                     i += 1
                 print("Жай сан" if is_prime else "Құрама сан")
                 ''')),
                ("Фибоначчи тізбегінің алғашқы N мүшесін шығарыңыз.",
                 C('''
                 n = int(input("N = "))
                 a, b = 0, 1
                 for _ in range(n):
                     print(a, end=" ")
                     a, b = b, a + b
                 ''')),
            ],
        },
    },
    "Тізімдер (Lists)": {
        "focus": "Тізім элементтеріне индекс және цикл арқылы дұрыс қол жеткізілген",
        "levels": {
            "🌱 Базалық": [
                ("5 санның тізімін енгізіңіз. Олардың қосындысы мен орташа мәнін табыңыз.",
                 C('''
                 a = [int(input()) for _ in range(5)]
                 print("Қосынды:", sum(a))
                 print("Орташа:", sum(a) / len(a))
                 ''')),
                ("Тізімдегі ең үлкен элементті және оның индексін табыңыз.",
                 C('''
                 a = [4, 17, 9, 25, 11]
                 m = max(a)
                 print("Ең үлкені:", m, "индексі:", a.index(m))
                 ''')),
            ],
            "🌿 Орта": [
                ("Тізімнен тек жұп сандарды жаңа тізімге жинап, шығарыңыз.",
                 C('''
                 a = [3, 8, 12, 7, 20, 5]
                 even = []
                 for x in a:
                     if x % 2 == 0:
                         even.append(x)
                 print(even)
                 ''')),
                ("Тізімді срезсіз және reverse() қолданбай, цикл арқылы кері айналдырыңыз.",
                 C('''
                 a = [1, 2, 3, 4, 5]
                 for i in range(len(a) // 2):
                     a[i], a[len(a) - 1 - i] = a[len(a) - 1 - i], a[i]
                 print(a)
                 ''')),
            ],
            "🌳 Жоғары": [
                ("Тізімді «көпіршік» әдісімен өсу ретімен сұрыптаңыз.",
                 C('''
                 a = [5, 2, 9, 1, 7]
                 n = len(a)
                 for i in range(n - 1):
                     for j in range(n - 1 - i):
                         if a[j] > a[j + 1]:
                             a[j], a[j + 1] = a[j + 1], a[j]
                 print(a)
                 ''')),
                ("Тізімнен қайталанатын элементтерді жойып, алғашқы ретті сақтаңыз.",
                 C('''
                 a = [3, 1, 3, 2, 1, 5, 2]
                 res = []
                 for x in a:
                     if x not in res:
                         res.append(x)
                 print(res)
                 ''')),
            ],
        },
    },
    "Функциялар": {
        "focus": "Функция дұрыс жарияланған, параметрлер мен return қолданылған",
        "levels": {
            "🌱 Базалық": [
                ("Санның квадратын қайтаратын square(x) функциясын жазыңыз.",
                 C('''
                 def square(x):
                     return x * x

                 print(square(7))
                 ''')),
                ("Оқушының атын параметр ретінде алып, сәлемдесетін функция жазыңыз.",
                 C('''
                 def hello(name):
                     print("Сәлем,", name + "!")

                 hello("Айым")
                 ''')),
            ],
            "🌿 Орта": [
                ("Сандар тізімінің орташа мәнін қайтаратын функция жазыңыз.",
                 C('''
                 def average(a):
                     return sum(a) / len(a)

                 print(average([4, 8, 6, 10]))
                 ''')),
                ("Сөздегі қазақ тілінің дауысты дыбыстарының санын қайтаратын функция жазыңыз.",
                 C('''
                 def count_vowels(word):
                     vowels = "аәеёиоөуұүыіэюя"
                     count = 0
                     for ch in word.lower():
                         if ch in vowels:
                             count += 1
                     return count

                 print(count_vowels("Информатика"))
                 ''')),
            ],
            "🌳 Жоғары": [
                ("Рекурсия арқылы n! (факториал) есептейтін функция жазыңыз.",
                 C('''
                 def fact(n):
                     if n <= 1:
                         return 1
                     return n * fact(n - 1)

                 print(fact(5))
                 ''')),
                ("Сөздің палиндром екенін тексеретін функция жазып, оны үш мысалмен тексеріңіз.",
                 C('''
                 def is_palindrome(s):
                     s = s.lower().replace(" ", "")
                     return s == s[::-1]

                 for w in ["Level", "Алма", "А роза упала на лапу Азора"]:
                     print(w, "→", is_palindrome(w))
                 ''')),
            ],
        },
    },
}


def criteria_rows(focus: str):
    return [
        ("Есептің шарты орындалған, нәтиже дұрыс", 2),
        (focus, 2),
        ("Код оқуға ыңғайлы (айнымалы атаулары, түсініктемелер)", 1),
        ("Бағдарлама әртүрлі енгізу мәндерімен тексерілген", 1),
    ]


def criteria_markdown(focus: str) -> str:
    rows = criteria_rows(focus)
    md = "| № | Критерий | Балл |\n|---|---|---|\n"
    for i, (name, pts) in enumerate(rows, 1):
        md += f"| {i} | {name} | {pts} |\n"
    md += "| | **Барлығы** | **6** |\n\n"
    md += "**Бағалау шкаласы:** 6 балл — «5» · 5 балл — «4» · 3–4 балл — «3» · 0–2 балл — «2»"
    return md


def demo_generate(topic: str, levels: list, variant: str) -> dict:
    data = TOPICS[topic]
    items = []
    for lvl in levels:
        pool = data["levels"][lvl]
        if variant == "Кездейсоқ":
            task, code = random.choice(pool)
        else:
            task, code = pool[0] if variant == "1-нұсқа" else pool[1]
        items.append({"level": lvl, "task": task, "code": code})
    return {
        "mode": "demo",
        "topic": topic,
        "items": items,
        "criteria": criteria_markdown(data["focus"]),
    }


def tasks_to_text(result: dict) -> str:
    out = [f"# Тақырып: {result['topic']}\n"]
    if result["mode"] == "llm":
        out.append(result["text"])
        return "\n".join(out)
    for i, it in enumerate(result["items"], 1):
        out.append(f"## Есеп {i} ({it['level']})\n{it['task']}\n")
        out.append("Шешуі:\n```python\n" + it["code"] + "\n```\n")
    out.append("## Бағалау критерийлері\n" + result["criteria"])
    return "\n".join(out)


# ─────────────────────────────────────────────────────────────
# 3. ЖИ (OpenAI) — МІНДЕТТІ ЕМЕС
# ─────────────────────────────────────────────────────────────

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b"


def get_api_settings():
    key = st.session_state.get("api_key", "").strip()
    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            key = ""
    if not key:
        key = os.environ.get("GROQ_API_KEY", "")
    model = (st.session_state.get("model_name") or DEFAULT_MODEL).strip()
    return key.strip(), model


def call_llm(system_prompt: str, user_prompt: str) -> str:
    key, model = get_api_settings()
    from openai import OpenAI  # Groq OpenAI-үйлесімді API қолдайды
    client = OpenAI(api_key=key, base_url=GROQ_BASE_URL)
    resp = client.chat.completions.create(
        model=model,
        temperature=0.5,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.choices[0].message.content


# ─────────────────────────────────────────────────────────────
# 4. КОДТЫ ТАЛДАУ (ДЕМО-РЕЖИМ: ережелерге негізделген)
# ─────────────────────────────────────────────────────────────

BLOCK_KW = ("if", "elif", "else", "for", "while", "def", "class",
            "try", "except", "finally", "with")

GENERIC_SYNTAX_KZ = {
    "invalid syntax": "Синтаксис дұрыс емес: жолда Python түсінбейтін символ немесе сөз бар.",
    "invalid decimal literal": "Санның жазылуы дұрыс емес (мысалы, айнымалы аты цифрдан басталып тұр).",
    "cannot assign to": "Мән меншіктеу мүмкін емес жерге «=» қойылған.",
    "positional argument follows keyword argument": "Атаулы аргументтен кейін қарапайым аргумент тұр.",
}


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _prev_nonblank(lines, idx):
    for j in range(idx - 1, -1, -1):
        if lines[j].strip():
            return j
    return None


def syntax_fix(lines, e):
    """Синтаксистік қатені түзетуге тырысады. Сәтті болса — issue қайтарады."""
    msg = e.msg or ""
    ln = max(0, min((e.lineno or 1) - 1, len(lines) - 1))
    line = lines[ln]
    stripped = line.strip()

    def issue(title, why):
        return {"line": ln + 1, "title": title, "why": why}

    # 1) Қос нүкте жетіспейді
    first_word = re.split(r"[\s(:]", stripped, maxsplit=1)[0] if stripped else ""
    if "expected ':'" in msg or (
        msg == "invalid syntax" and first_word in BLOCK_KW and not stripped.endswith(":")
    ) or (msg == "expected ':'"):
        if not stripped.endswith(":"):
            lines[ln] = line.rstrip() + ":"
            return issue(
                "Жол соңында қос нүкте «:» жоқ",
                f"`{first_word}` сияқты блок ашатын операторлардан кейін міндетті түрде "
                "қос нүкте қойылады. Қос нүкте Python-ға «төменде осы шартқа/циклге тиесілі "
                "код блогы басталады» дегенді білдіреді.",
            )

    # 2) Жабылмаған жақша
    m = re.search(r"'(.)' was never closed", msg)
    if m or "unexpected EOF" in msg:
        opener = m.group(1) if m else "("
        closer = {"(": ")", "[": "]", "{": "}"}.get(opener, ")")
        lines[ln] = line.rstrip() + closer
        return issue(
            f"Ашылған «{opener}» жақшасы жабылмаған",
            f"Әр ашылған жақшаға жабылатын жақша керек. Жолдың соңына «{closer}» қосылды. "
            "Жақшалар санын тексеру әдетке айналсын: ашылғандар саны = жабылғандар саны.",
        )

    # 3) Жабылмаған жол (кавычка)
    if "unterminated string literal" in msg or "EOL while scanning string literal" in msg:
        q = None
        if e.offset and 0 < e.offset <= len(line) and line[e.offset - 1] in "\"'":
            q = line[e.offset - 1]
        if q is None:
            mq = re.search(r"[\"']", line)
            q = mq.group(0) if mq else '"'
        lines[ln] = line.rstrip() + q
        return issue(
            "Мәтін (жол) тырнақшасы жабылмаған",
            f"Мәтін тырнақшамен басталса, оны сол тырнақшамен жабу керек. Жолдың соңына «{q}» қосылды.",
        )

    # 4) Python 2 стиліндегі print
    if "Missing parentheses in call to 'print'" in msg:
        mp = re.match(r"^(\s*)print\s+(.*)$", line)
        if mp:
            lines[ln] = f"{mp.group(1)}print({mp.group(2).rstrip()})"
            return issue(
                "print функциясы жақшасыз жазылған",
                "Python 3-те print — функция, сондықтан аргументтер жақша ішінде жазылады: "
                "`print(\"мәтін\")`.",
            )

    # 5) Шартта «=» орнына «==»
    cond = re.match(r"^(\s*)(if|elif|while)\b(.*):\s*$", line)
    if cond and ("Maybe you meant '=='" in msg or msg == "invalid syntax"
                 or "cannot assign" in msg):
        new_cond = re.sub(r"(?<![=!<>])=(?!=)", "==", cond.group(3))
        if new_cond != cond.group(3):
            lines[ln] = f"{cond.group(1)}{cond.group(2)}{new_cond}:"
            return issue(
                "Шартта «=» орнына «==» қолданылуы керек",
                "«=» — мән меншіктеу операторы, ал «==» — тең екенін салыстыру операторы. "
                "Шарттың ішінде салыстыру үшін әрқашан «==» жазылады.",
            )

    # 6) Шегініс қателері
    if "expected an indented block" in msg:
        pj = _prev_nonblank(lines, ln)
        base = _indent_of(lines[pj]) if pj is not None else 0
        lines[ln] = " " * (base + 4) + stripped
        return issue(
            "Блок ішінде шегініс жоқ",
            "if, for, while, def сияқты операторлардан кейінгі жол ішке қарай (4 бос орынмен) "
            "жылжытылып жазылуы керек. Шегініс — Python-да кодтың құрылымын көрсетеді.",
        )

    if "unexpected indent" in msg:
        pj = _prev_nonblank(lines, ln)
        base = _indent_of(lines[pj]) if pj is not None else 0
        lines[ln] = " " * base + stripped
        return issue(
            "Артық шегініс",
            "Алдыңғы жол қос нүктемен аяқталмаса, келесі жолды ішке жылжытуға болмайды. "
            "Артық бос орындар алынды.",
        )

    if "unindent does not match" in msg:
        cur = _indent_of(line)
        prevs = sorted({_indent_of(l) for l in lines[:ln] if l.strip()})
        smaller = [p for p in prevs if p < cur]
        target = smaller[-1] if smaller else 0
        lines[ln] = " " * target + stripped
        return issue(
            "Шегініс деңгейі сәйкес емес",
            "Жолдың шегінісі алдыңғы блоктардың ешқайсысымен сәйкес келмейді. "
            "Шегіністі басқа жолдармен бір деңгейге келтірдік.",
        )

    return None


def semantic_checks(lines):
    """Синтаксис дұрыс болғаннан кейінгі қарапайым тексерулер."""
    issues = []
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError:
        return issues

    # --- анықталған аттар
    defined = set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            defined.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.arg):
            defined.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                defined.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            defined.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            defined.update(node.names)

    # --- 1) Анықталмаған аттар (мысалы, pritn)
    seen = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id not in defined:
            key = (node.lineno, node.id)
            if key in seen:
                continue
            seen.add(key)
            match = difflib.get_close_matches(node.id, list(defined), n=1, cutoff=0.75)
            if match:
                new = match[0]
                lines[node.lineno - 1] = re.sub(rf"\b{re.escape(node.id)}\b", new, lines[node.lineno - 1])
                issues.append({
                    "line": node.lineno,
                    "title": f"«{node.id}» аты танылмады — «{new}» болуы мүмкін",
                    "why": f"Python `{node.id}` дегенді білмейді (NameError). Ең ұқсас атау — `{new}`, "
                           "яғни, ол жерде әріп қатесі кеткен. Түзетілді.",
                })
            else:
                issues.append({
                    "line": node.lineno,
                    "title": f"«{node.id}» айнымалысы жарияланбаған",
                    "why": f"`{node.id}` атына дейін мән берілмеген (NameError). Айнымалыны қолданудан бұрын "
                           "оған мән беріңіз немесе атының дұрыс жазылғанын тексеріңіз.",
                    "nofix": True,
                })

    # --- 2) input() нәтижесі санға айналдырылмаған
    input_vars = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "input"):
            input_vars[node.targets[0].id] = node.lineno

    def is_in(n):
        return isinstance(n, ast.Name) and n.id in input_vars

    def is_num(n):
        return isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool)

    flagged = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            l, r = node.left, node.right
            arith = isinstance(node.op, (ast.Sub, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow))
            if arith:
                for side in (l, r):
                    if is_in(side):
                        flagged[side.id] = node.lineno
            elif isinstance(node.op, ast.Add):
                if (is_in(l) and (is_num(r) or is_in(r))) or (is_in(r) and is_num(l)):
                    for side in (l, r):
                        if is_in(side):
                            flagged[side.id] = node.lineno
            elif isinstance(node.op, ast.Mult):
                if is_in(l) and is_in(r):
                    flagged[l.id] = node.lineno
                    flagged[r.id] = node.lineno
        elif isinstance(node, ast.Compare):
            parts = [node.left] + node.comparators
            if any(is_in(p) for p in parts) and any(is_num(p) for p in parts):
                for p in parts:
                    if is_in(p):
                        flagged[p.id] = node.lineno

    for var, use_line in flagged.items():
        aln = input_vars[var]
        old = lines[aln - 1]
        new = re.sub(r"input\(([^()]*)\)", r"int(input(\1))", old, count=1)
        if new != old:
            lines[aln - 1] = new
            issues.append({
                "line": aln,
                "title": f"«{var}» айнымалысы мәтін күйінде қалып қойған",
                "why": f"`input()` әрқашан мәтін (str) қайтарады. `{var}` айнымалысы {use_line}-жолда "
                       "сан ретінде қолданылған, сондықтан не қате шығады (TypeError), не сандар қосылмай, "
                       "жапсырылып қалады (мысалы, \"2\" + \"3\" = \"23\"). `int(...)` арқылы бүтін санға "
                       "айналдырдық; егер бөлшек сан керек болса, `float(...)` қолданыңыз.",
            })

    return issues


def analyze_code(code: str) -> dict:
    lines = code.replace("\t", "    ").split("\n")
    original = list(lines)
    issues = []
    unresolved = None

    for _ in range(20):
        try:
            compile("\n".join(lines), "<kod>", "exec")
            unresolved = None
            break
        except SyntaxError as e:
            res = syntax_fix(lines, e)
            if res is None:
                unresolved = e
                break
            issues.append(res)
    else:
        unresolved = None

    if unresolved is None:
        issues.extend(semantic_checks(lines))

    changed = []
    for i, (a, b) in enumerate(zip(original, lines), 1):
        if a != b:
            changed.append((i, a, b))

    return {
        "issues": sorted(issues, key=lambda x: x["line"]),
        "fixed": "\n".join(lines),
        "changed": changed,
        "unresolved": unresolved,
    }


def explain_unresolved(e: SyntaxError) -> str:
    msg = e.msg or "Белгісіз қате"
    for key, kz in GENERIC_SYNTAX_KZ.items():
        if key in msg:
            return kz
    return "Python бұл жолды түсіне алмады. Жолдағы жақшаларды, тырнақшаларды, операторларды және әріптердің жазылуын тексеріңіз."


# ─────────────────────────────────────────────────────────────
# 5. БЕТТЕР
# ─────────────────────────────────────────────────────────────

def page_home():
    st.markdown(
        """
<div class="hero">
<h1>🎓 ИнфоАссистент</h1>
<p>Информатика мұғалімдеріне арналған цифрлық көмекші. Python тілінен деңгейлік
тапсырмаларды бірнеше секундта дайындаңыз, оқушылардың кодындағы қатені тауып,
қазақ тілінде түсіндіріңіз — уақытыңызды сабаққа және оқушыларыңызға қалдырыңыз.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
<div class="feature">
<div class="icon">📝</div>
<h3>Тапсырмалар генераторы</h3>
<p>Тақырыпты таңдаңыз — үш деңгейлік есептер, дайын шешу жолдары және
бағалау критерийлері бірден шығады.</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
<div class="feature warm">
<div class="icon">🐞</div>
<h3>Қатемен жұмыс</h3>
<p>Қате жазылған кодты енгізіңіз — қатенің қай жолда екенін көрсетіп,
қазақ тілінде түсіндіріп, түзетілген нұсқасын береді.</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
<div class="feature teal">
<div class="icon">⏱️</div>
<h3>Уақытты үнемдеу</h3>
<p>Сабаққа дайындалу, үй тапсырмасын тексеру және оқушымен қатені талдау
енді әлдеқайда жеңіл әрі жылдам.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("### 🚀 Қалай бастаймыз?")
    st.markdown('<div class="step">1️⃣ Сол жақтағы мәзірден қажетті бөлімді таңдаңыз.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step">2️⃣ Тақырыпты таңдаңыз немесе кодты енгізіңіз.</div>', unsafe_allow_html=True)
    st.markdown('<div class="step">3️⃣ Батырманы басыңыз — нәтижені бірден көресіз. Тапсырмаларды файл ретінде жүктеп алуға болады.</div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="warm-note">
💛 <b>Кеңес:</b> сайт қосымшасыз да (демо-режимде) жұмыс істейді. Ал бүйір мәзірде
Groq API кілтін енгізсеңіз, тапсырмалар мен қате талдауы нақты жасанды интеллект арқылы жасалады.
</div>
""",
        unsafe_allow_html=True,
    )


def render_task_result(result: dict):
    st.markdown(f"#### 📚 Тақырып: {result['topic']}")

    if result["mode"] == "llm":
        st.markdown(result["text"])
    else:
        for i, it in enumerate(result["items"], 1):
            cls = LEVELS[it["level"]]
            st.markdown(
                f"""
<div class="task-card {cls}">
<span class="badge {cls}">{it['level']}</span>
<h4>Есеп {i}</h4>
<p>{html.escape(it['task'])}</p>
</div>
""",
                unsafe_allow_html=True,
            )
            with st.expander("💡 Шешу жолын көрсету"):
                st.code(it["code"], language="python")

        st.markdown("#### 🏅 Бағалау критерийлері")
        st.markdown(result["criteria"])

    st.download_button(
        "⬇️ Тапсырмаларды жүктеп алу (.md)",
        data=tasks_to_text(result).encode("utf-8"),
        file_name="tapsyrmalar.md",
        mime="text/markdown",
    )


def page_generator():
    st.markdown('<div class="page-title">📝 Тапсырмалар генераторы</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Python тілінің тақырыбын таңдаңыз — оқушыларға арналған деңгейлік есептерді, '
        'шешу жолдарын және бағалау критерийлерін дайындаймыз.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        topic = st.selectbox("📚 Тақырыпты таңдаңыз", list(TOPICS.keys()))
    with col2:
        variant = st.radio("🔀 Нұсқа", ["1-нұсқа", "2-нұсқа", "Кездейсоқ"], horizontal=True)

    levels = st.multiselect(
        "🎚️ Қиындық деңгейлері",
        list(LEVELS.keys()),
        default=list(LEVELS.keys()),
    )

    if st.button("✨ Тапсырма жасау"):
        if not levels:
            st.warning("Кемінде бір деңгейді таңдаңыз.")
        else:
            key, _ = get_api_settings()
            if key:
                try:
                    with st.spinner("ЖИ тапсырмаларды дайындап жатыр..."):
                        sys_p = ("Сен тәжірибелі информатика мұғалімісің. Барлық жауабыңды қазақ тілінде, "
                                 "Markdown форматында жаз.")
                        usr_p = (f"Python тілінен «{topic}» тақырыбы бойынша мына деңгейлерге есептер құрастыр: "
                                 f"{', '.join(levels)}. Әр деңгейге 1 есептен бер. Әр есептің астында "
                                 "```python``` блогында шешу жолын көрсет. Соңында 6 баллдық бағалау "
                                 "критерийлерін кесте түрінде бер.")
                        text = call_llm(sys_p, usr_p)
                    st.session_state["task_result"] = {"mode": "llm", "topic": topic, "text": text}
                except Exception as exc:
                    st.error(f"ЖИ-ге қосылу мүмкін болмады ({exc}). Демо-режимге ауыстық.")
                    st.session_state["task_result"] = demo_generate(topic, levels, variant)
            else:
                st.session_state["task_result"] = demo_generate(topic, levels, variant)
            st.balloons()

    if "task_result" in st.session_state:
        st.markdown("---")
        render_task_result(st.session_state["task_result"])


def render_debug_result(code: str, res: dict):
    issues = res["issues"]
    unresolved = res["unresolved"]

    if not issues and unresolved is None:
        st.success("🎉 Синтаксистік қателер табылмады, код дұрыс көрінеді!")
        st.info("Ескерту: демо-режим логикалық қателерді (дұрыс емес нәтиже беретін формуланы) таба алмайды. "
                "Мұндай жағдайда кодты бірнеше мәнмен тексеріңіз немесе бүйір мәзірде ЖИ режимін қосыңыз.")
        return

    if issues:
        st.markdown(f"### 🔍 Табылған қателер: {len(issues)}")
        for it in issues:
            st.markdown(
                f"""
<div class="issue">
<div class="where">📍 {it['line']}-жол</div>
<div class="title">{html.escape(it['title'])}</div>
<div class="why">{html.escape(it['why'])}</div>
</div>
""",
                unsafe_allow_html=True,
            )

    if unresolved is not None:
        line_no = unresolved.lineno or "?"
        st.error(f"⚠️ {line_no}-жолда түзету қиын қате қалды: {unresolved.msg}")
        st.markdown(f"**Түсіндірме:** {explain_unresolved(unresolved)}")
        if unresolved.text:
            st.code(unresolved.text.rstrip("\n"), language="python")
        st.caption("Төмендегі нұсқада мына жолға дейінгі қателер түзетілді; қалғанын қолмен түзетіңіз.")

    if res["changed"]:
        st.markdown("### 🔧 Не өзгерді?")
        for ln, old, new in res["changed"]:
            st.markdown(
                f'<div class="diff-row diff-old">{ln}-жол − {html.escape(old)}</div>'
                f'<div class="diff-row diff-new">{ln}-жол + {html.escape(new)}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("### ✅ Түзетілген нұсқа")
    st.code(res["fixed"], language="python")
    st.markdown(
        '<div class="warm-note">💛 Оқушыға кеңес: түзетілген кодты көшіріп алудың орнына, '
        'қатені өзі түсініп, қайта жазып көрсін — осылай ол ең жақсы үйренеді.</div>',
        unsafe_allow_html=True,
    )


EXAMPLE_CODE = '''a = input("Бірінші сан: ")
b = input("Екінші сан: ")
if a > 0
    print("Қосынды:", a + b)
else:
    pritn("Оң сан емес")'''


def page_debugger():
    st.markdown('<div class="page-title">🐞 Қатемен жұмыс / Кодты талдау</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Қате жазылған Python кодын енгізіңіз — қатенің қайда екенін табамыз, '
        'қазақша түсіндіреміз және дұрыс нұсқасын көрсетеміз.</div>',
        unsafe_allow_html=True,
    )

    if "code_input" not in st.session_state:
        st.session_state["code_input"] = ""

    if st.button("📋 Мысал кодты қою"):
        st.session_state["code_input"] = EXAMPLE_CODE

    code = st.text_area(
        "✍️ Python кодыңызды осында жазыңыз",
        key="code_input",
        height=260,
        placeholder="print('Сәлем, әлем!'",
    )

    if st.button("🔎 Қатені табу және түсіндіру"):
        if not code.strip():
            st.warning("Алдымен код енгізіңіз.")
            return

        st.markdown("---")
        key, _ = get_api_settings()
        if key:
            try:
                with st.spinner("ЖИ кодты талдап жатыр..."):
                    sys_p = ("Сен - информатика пәнінің мұғаліміне арналған зияткерлік цифрлық көмекшісің. "
                             "Төменде берілген Python кодын мұқият талдап шық. Бар болған қателерді "
                             "(SyntaxError, NameError, TypeError, логикалық қателер т.б.) анықта. "
                             "Жауапты тек таза қазақ тілінде, оқушыға немесе мұғалімге өте түсінікті, "
                             "дос пейілмен жаз.")
                    usr_p = ("Код:\n```python\n" + code + "\n```\n\n"
                             "Жауабыңды мына құрылыммен бер:\n"
                             "## 🔍 Қате қай жерде (жол нөмірімен және қате түрімен)\n"
                             "## 💡 Қазақша түсіндірме (неге қате болды)\n"
                             "## ✅ Түзетілген код (толық, ```python``` блогында)\n"
                             "## 📝 Оқушыға кеңес")
                    answer = call_llm(sys_p, usr_p)
                st.markdown(answer)
                return
            except Exception as exc:
                st.error(f"ЖИ-ге қосылу мүмкін болмады ({exc}). Демо-режимге ауыстық.")

        with st.spinner("Код талданып жатыр..."):
            res = analyze_code(code)
        render_debug_result(code, res)


# ─────────────────────────────────────────────────────────────
# 6. НЕГІЗГІ БАҒДАРЛАМА
# ─────────────────────────────────────────────────────────────

PAGES = {
    "🏠 Басты бет": page_home,
    "📝 Тапсырмалар генераторы": page_generator,
    "🐞 Қатемен жұмыс": page_debugger,
}


def main():
    with st.sidebar:
        st.markdown(
            """
<div class="brand">
<div class="logo">🎓</div>
<div class="name">ИнфоАссистент</div>
<div class="slogan">Мұғалімнің цифрлық көмекшісі</div>
</div>
""",
            unsafe_allow_html=True,
        )
        choice = st.radio("Бөлімдер", list(PAGES.keys()), label_visibility="collapsed")

        st.markdown("---")
        with st.expander("⚙️ ЖИ баптаулары"):
            st.text_input("Groq API кілті", type="password", key="api_key",
                          help="Бос қалдырсаңыз, демо-режим қолданылады.")
            st.text_input("Модель", value=DEFAULT_MODEL, key="model_name")
            key, _ = get_api_settings()
            st.caption("Күй: " + ("🟢 ЖИ режимі" if key else "🟡 Демо-режим"))

    PAGES[choice]()

    st.markdown(
        '<div class="footer">💜 Информатика мұғалімдері үшін жасалған · Python + Streamlit</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
