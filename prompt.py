def get_prompt_intro():
    return """You are an expert in statistics, econometrics and data mining.

Your task is to recommend the 10 most suitable journals (ranked from most to least suitable)
from the predefined candidate list below, based strictly and exclusively on the information
explicitly provided in the input academic article.

IMPORTANT CONSTRAINTS:
- You must base your recommendation ONLY on the given Title, Abstract, Keywords.
- You are NOT allowed to use any prior knowledge, memorized information, or familiarity about this paper,
  its authors, or any real-world publication or submission outcomes.
- Do NOT rely on general reputation, impact, or historical publishing patterns of journals
  beyond what can be inferred from the provided text itself.
- You must not use web search or external information sources.

TASK INTERPRETATION:
- Treat each candidate journal as a semantic profile defined by its stated scope description,
  rather than as a real-world journal entity.
- Your goal is to assess semantic compatibility between the input article and each journal’s scope,
  not to recall where similar papers are usually published.
"""

def get_prompt_guide():
    return """When deciding, consider ONLY the following aspects as inferred from the provided text:
- The methodological focus (e.g., theoretical statistics, applied statistics, statistical methodology, 
computational and algorithmic statistics, biostatistics and medical statistics, economic and business statistics, 
engineering and information systems, machine learning and artificial intelligence)
- The scientific or application domain (e.g., economics, business, finance, biology and life sciences, medicine and public health, 
social sciences, engineering, physical sciences, and information sciences)
- The intended academic audience, as reflected by terminology, keywords, and cited literature
"""

def get_prompt_article_block(title, abstract, keywords):
    return f"""
Now, consider the following academic article:

---
**Title**: {title}

**Abstract**:
{abstract}

**Keywords**: {keywords}
---
"""

def get_prompt_format():
    return """
OUTPUT REQUIREMENTS:
- Rank exactly 10 journals from the candidate list, ordered from most to least suitable.
- Use the exact journal names as provided in the candidate list.
- Do NOT include explanations, justifications, citations, or any text beyond the ranked list.

Format your output as:
RECOMMENDATION_1: <journal name>
RECOMMENDATION_2: <journal name>
RECOMMENDATION_3: <journal name>
RECOMMENDATION_4: <journal name>
RECOMMENDATION_5: <journal name>
RECOMMENDATION_6: <journal name>
RECOMMENDATION_7: <journal name>
RECOMMENDATION_8: <journal name>
RECOMMENDATION_9: <journal name>
RECOMMENDATION_10: <journal name>
"""

def construct_prompt(title, abstract, keywords, journal_scope, journal_options):
    """
    Assemble the full prompt from modular parts.
    """
    return f"""{get_prompt_intro()}
{get_prompt_guide()}
{journal_scope}

Candidate Journals:
{journal_options}
{get_prompt_article_block(title, abstract, keywords)}
{get_prompt_format()}"""