import json
from ai.config.llm_config import get_llm
from ai.prompts.outline_prompt import OUTLINE_PROMPT


def parse_json(text):
    text = text.strip()
    if "```" in text:
        text = text.split("```")[1].lstrip("json").strip()
    start = text.find("{")
    end   = text.rfind("}") + 1
    return json.loads(text[start:end])


def make_research_summary(research):
    """Compact summary of research for outline prompt."""
    lines = []

    for r in research[:5]:
        title = r.get("title", "")
        raw_points = r.get("key_points", [])[:2]

        points = []
        for p in raw_points:
            if isinstance(p, dict):
                val = p.get("point", "")
                if val:
                    points.append(str(val))
            else:
                points.append(str(p))

        if not points:
            points = ["no data"]

        lines.append(f"- {title}: {' | '.join(points)}")

    return "\n".join(lines) if lines else "No research available"


def normalize_outline(outline, topic, blog_type="informational"):
    title = (outline or {}).get("title") or f"{topic}: practical guide"
    raw_sections = (outline or {}).get("sections") or []
    sections = []

    for section in raw_sections:
        if not isinstance(section, dict):
            continue

        heading = str(section.get("heading", "")).strip()
        subsections = section.get("subsections", section.get("subtopics", []))
        if isinstance(subsections, str):
            subsections = [subsections]
        if not isinstance(subsections, list):
            subsections = []

        cleaned_subsections = [
            str(item).strip() for item in subsections if str(item).strip()
        ][:4]

        if heading:
            sections.append({
                "heading": heading,
                "subsections": cleaned_subsections,
            })

    if len(sections) < 5:
        sections = fallback_outline(topic, blog_type)

    sections = enforce_faq_section(sections, topic)

    return {
        "title": str(title).strip(),
        "sections": sections[:8],
    }


def fallback_outline(topic, blog_type="informational"):
    category_sections = {
        "comparison": [
            {
                "heading": f"Which {topic} options solve the real problem best",
                "subsections": [
                    "What buyers usually get wrong first",
                    "What matters most before comparing tools",
                ],
            },
            {
                "heading": f"How the top {topic} options differ in real use",
                "subsections": [
                    "Where each option feels faster or easier",
                    "Where limitations show up quickly",
                ],
            },
            {
                "heading": f"{topic} comparison table: features, speed, and fit",
                "subsections": [
                    "Side-by-side differences",
                    "Best fit by workflow",
                ],
            },
            {
                "heading": f"Workflow-based comparison for {topic}",
                "subsections": [
                    "Best choice for beginners",
                    "Best choice for advanced users or teams",
                ],
            },
            {
                "heading": f"Who should choose which {topic} option",
                "subsections": [
                    "Decision guide by budget or goal",
                    "When switching tools is worth it",
                ],
            },
            {
                "heading": f"Common mistakes when comparing {topic}",
                "subsections": [
                    "Misleading evaluation criteria",
                    "Trade-offs people ignore until later",
                ],
            },
        ],
        "listicle": [
            {
                "heading": f"Which {topic} options are actually worth shortlisting",
                "subsections": [
                    "What separates top picks from average ones",
                    "Why ranking depends on use case",
                ],
            },
            {
                "heading": f"Top {topic} picks and what each one does best",
                "subsections": [
                    "Best overall option",
                    "Best option for specialized needs",
                ],
            },
            {
                "heading": f"How to choose the right {topic} from this list",
                "subsections": [
                    "Signals that narrow your shortlist fast",
                    "How to avoid paying for the wrong fit",
                ],
            },
            {
                "heading": f"Best workflows for using these {topic} picks",
                "subsections": [
                    "Where setup effort pays off",
                    "Where simple tools outperform advanced ones",
                ],
            },
            {
                "heading": f"Trade-offs and limitations across these {topic} options",
                "subsections": [
                    "What quality or speed usually costs",
                    "Where the list leader is not the best choice",
                ],
            },
            {
                "heading": f"Mistakes people make when choosing {topic} from top lists",
                "subsections": [
                    "Why feature count can mislead decisions",
                    "How to validate before committing",
                ],
            },
        ],
        "guide": [
            {
                "heading": f"Where most people get stuck with {topic}",
                "subsections": [
                    "What makes the first step confusing",
                    "What to prepare before starting",
                ],
            },
            {
                "heading": f"How {topic} works without the usual jargon",
                "subsections": [
                    "Core pieces that affect outcomes",
                    "How to think about quality versus speed",
                ],
            },
            {
                "heading": f"A step-by-step workflow to get better results with {topic}",
                "subsections": [
                    "What to do first",
                    "How to improve weak output",
                ],
            },
            {
                "heading": f"When to use different approaches for {topic}",
                "subsections": [
                    "Best path for beginners",
                    "When advanced setups are worth it",
                ],
            },
            {
                "heading": f"Mistakes that make {topic} harder than it should be",
                "subsections": [
                    "What causes poor output quality",
                    "How to correct issues early",
                ],
            },
            {
                "heading": f"How to decide your next step with {topic}",
                "subsections": [
                    "What to keep doing",
                    "What to test next",
                ],
            },
        ],
        "review": [
            {
                "heading": f"Is {topic} actually worth using",
                "subsections": [
                    "Who gets value quickly",
                    "Who will hit limits fast",
                ],
            },
            {
                "heading": f"What {topic} does well and where it falls short",
                "subsections": [
                    "Strongest capabilities",
                    "Weak spots that matter in real use",
                ],
            },
            {
                "heading": f"How {topic} performs in real workflows",
                "subsections": [
                    "Best-case usage scenarios",
                    "Where friction shows up",
                ],
            },
            {
                "heading": f"How {topic} compares to close alternatives",
                "subsections": [
                    "What makes it stand out",
                    "When an alternative is the smarter pick",
                ],
            },
            {
                "heading": f"Who should choose {topic} and who should skip it",
                "subsections": [
                    "Best-fit user profile",
                    "Red flags before committing",
                ],
            },
            {
                "heading": f"Common mistakes when evaluating {topic}",
                "subsections": [
                    "What early demos can hide",
                    "How to test it properly",
                ],
            },
        ],
    }

    default_sections = [
        {
            "heading": f"What makes {topic} confusing for buyers or beginners",
            "subsections": [
                "Where expectations usually break",
                "What users actually need before choosing",
            ],
        },
        {
            "heading": f"How {topic} works in real workflows",
            "subsections": [
                "Core moving parts that change results",
                "Where teams lose time or quality",
            ],
        },
        {
            "heading": f"Which tools, approaches, or options matter most for {topic}",
            "subsections": [
                "Best fit by use case",
                "Trade-offs that affect output quality",
            ],
        },
        {
            "heading": f"A practical workflow to get better results with {topic}",
            "subsections": [
                "Step-by-step process",
                "Checks before publishing or shipping",
            ],
        },
        {
            "heading": f"{topic} comparison: fastest path vs highest-quality path",
            "subsections": [
                "Where speed wins",
                "Where depth and accuracy matter more",
            ],
        },
        {
            "heading": f"Common mistakes that make {topic} output weaker",
            "subsections": [
                "Signs your process is too generic",
                "How to fix weak sections quickly",
            ],
        },
    ]

    sections = category_sections.get(blog_type, default_sections)
    return enforce_faq_section(sections, topic)


def enforce_faq_section(sections, topic):
    faq_heading_options = {"faq", "frequently asked questions"}
    normalized_sections = list(sections)

    faq_section = None
    non_faq_sections = []
    for section in normalized_sections:
        heading = str(section.get("heading", "")).strip()
        if heading.lower() in faq_heading_options or "faq" in heading.lower():
            faq_section = section
        else:
            non_faq_sections.append(section)

    faq_subsections = []
    if faq_section:
        faq_subsections = faq_section.get("subsections", [])
        if isinstance(faq_subsections, str):
            faq_subsections = [faq_subsections]

    cleaned_faq = [str(item).strip() for item in faq_subsections if str(item).strip()]
    fallback_faq = [
        f"What is the best way to start with {topic}?",
        f"How long does it take to get results from {topic}?",
        f"What are the biggest mistakes people make with {topic}?",
        f"How do I improve quality when using {topic}?",
        f"When should I choose a different approach instead of {topic}?",
    ]

    merged_faq = (cleaned_faq + fallback_faq)[:8]
    if len(merged_faq) < 5:
        merged_faq = fallback_faq

    non_faq_sections.append({
        "heading": "FAQ",
        "subsections": merged_faq[:8],
    })
    return non_faq_sections


def outline_agent(state):
    plan     = state.get("plan", {})
    keywords = state.get("keywords", {})
    research = state.get("research", [])

    llm = get_llm(fast=True)

    prompt = (
        OUTLINE_PROMPT
        .replace("{topic}", state.get("topic", ""))
        .replace("{blog_type}", plan.get("blog_type", "informational"))
        .replace("{tone}", plan.get("tone", "professional"))
        .replace("{target_audience}", plan.get("target_audience", "general readers"))
        .replace("{goal}", plan.get("goal", "help the reader make a confident decision"))
        .replace("{content_angle}", plan.get("content_angle", "practical and search-intent aligned"))
        .replace("{primary_keywords}", json.dumps(keywords.get("primary_keywords", [])[:3]))
        .replace("{secondary_keywords}", json.dumps(keywords.get("secondary_keywords", [])[:5]))
        .replace("{research_summary}", make_research_summary(research))
    )

    raw = llm.invoke(prompt).content
    print("\n[RAW OUTLINE OUTPUT]\n", raw[:300])

    try:
        outline = normalize_outline(
            parse_json(raw),
            state["topic"],
            plan.get("blog_type", "informational"),
        )
    except Exception as e:
        print(f"⚠️ Outline parse failed: {e}")
        outline = {
            "title": f"{state['topic']}: practical guide",
            "sections": fallback_outline(state["topic"], plan.get("blog_type", "informational")),
        }

    print("\n================ OUTLINE OUTPUT ================\n")
    print(outline)

    state["outline"] = outline
    return state
