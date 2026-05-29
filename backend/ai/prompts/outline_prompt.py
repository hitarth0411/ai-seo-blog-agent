OUTLINE_PROMPT = """ 
You are a senior SEO strategist.

Generate a HIGH-CONVERSION blog outline with EXACTLY 6–8 sections.

========================
INPUT
=====

Topic: {topic}
Blog type: {blog_type}
Tone: {tone}
Target audience: {target_audience}
Goal: {goal}
Content angle: {content_angle}
Primary keywords: {primary_keywords}
Secondary keywords: {secondary_keywords}
Research summary: {research_summary}

========================
CORE RULE (MOST IMPORTANT)
==========================

Every heading MUST be:

✔ Decision-driven OR
✔ Scenario-based OR
✔ Problem-solving

❌ NOT descriptive
❌ NOT informational-only

---

========================
STRICT HEADING RULES
====================

❌ BAN THESE PATTERNS:

* Why X matters
* Overview of X
* Key features
* Benefits of X
* Use cases
* Best practices
* Tips

👉 If heading sounds like a blog template → REJECT

---

========================
MANDATORY STRUCTURE
===================

You MUST adapt structure to blog type while staying decision-driven and SEO-friendly.

For ALL blog types include:
1. Reader problem / confusion
2. Core breakdown tied to search intent
3. Practical workflow, framework, or implementation section
4. Decision / recommendation section
5. Mistakes, limitations, or trade-offs
6. FAQ as the LAST section

Category guidance:
- comparison:
  include direct comparison, workflow comparison, and decision section
- listicle:
  include ranking logic, best-fit scenarios, and trade-off section
- guide:
  include step-by-step workflow and common mistakes
- review:
  include strengths, weaknesses, best-fit user, and alternatives
- informational:
  include clear explanations, real examples, and practical application

---

========================
COMPARISON BLOG HARD RULE
=========================

If blog_type = "comparison":

* MUST include tool names in headings
* MUST include:
  ✔ direct comparison
  ✔ workflow-based comparison
  ✔ decision section

---

========================
SUBSECTION RULE
===============

Each section MUST have 2–4 subsections except FAQ.

✔ specific
✔ concrete
✔ non-generic

Bad:

* Features
* Benefits

Good:

* “How Cursor handles multi-file context vs Claude Code limitations”

FAQ RULE:
- The last section heading must be exactly one of:
  - FAQ
  - Frequently Asked Questions
- FAQ section must contain 5–8 short question-style subsections
- Each FAQ subsection should read like a real search query

---

========================
TITLE RULE
==========

* Must include primary keyword
* Must sound like real search query

---

========================
FINAL CHECK
===========

For EACH heading:

* Can it be used for another topic?
  → YES → DELETE

* Does it help user decide something?
  → NO → REWRITE

---

========================
OUTPUT FORMAT (STRICT)
======================

Return ONLY valid JSON.

{{
"title": "",
"sections": [
{{
"heading": "",
"subsections": []
}}
]
}}
"""
