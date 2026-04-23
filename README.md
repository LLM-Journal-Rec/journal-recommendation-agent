# Journal Recommendation Agent

A prompt-based journal recommendation system powered by LLMs. Given a manuscript's title, abstract, and keywords, the agent recommends the top-10 most suitable journals from a predefined candidate list based on semantic compatibility.

---

## Project Structure

```
journal-agent/
├── agent.py                 # Core Agent class
├── prompt.py                # Prompt construction module
├── example.py               # Interactive usage script
├── data/
│   ├── journal_scope.csv    # Journal scope descriptions
│   └── papers.csv           # (Optional) Input papers for batch recommendation
├── requirements.txt         # Dependencies
└── README.md
```

---

## Requirements

- Python 3.8+
- An API key from [DeepSeek](https://platform.deepseek.com/) or [OpenAI](https://platform.openai.com/)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Data Format

### `journal_scope.csv`
Must contain exactly two columns:

| Journal | Scope |
|--------|-------|
| Annals of Statistics | Publishes research papers in all areas of statistics... |
| Journal of Machine Learning Research | Covers all areas of machine learning... |

### `papers.csv` (for batch recommendation)
Must contain the following three columns:

| title | abstract | keywords |
|-------|----------|----------|
| A Bayesian Approach to... | This paper proposes... | Bayesian, inference, statistics |

---

## Usage

### Step 1: Configure your API key

Open `example.py` and fill in your API key and file paths:

```python
API_KEY = "your-api-key-here"
SCOPE_CSV_PATH = "data/journal_scope.csv"
BASE_URL = "https://api.deepseek.com/v1"  # or https://api.openai.com/v1 for OpenAI
```

### Step 2: Run the agent

```bash
python example.py
```

You will be prompted to choose a mode:

```
==================================================
   Journal Recommendation Agent
==================================================
Please select a mode:
  [1] Single article recommendation
  [2] Batch recommendation (from CSV)
==================================================
```

---

## Example Output

### Single Article Mode

```
Top-10 Recommended Journals:
----------------------------------------
  RECOMMENDATION_1:  Annals of Statistics
  RECOMMENDATION_2:  Journal of the American Statistical Association
  RECOMMENDATION_3:  Biometrika
  RECOMMENDATION_4:  Journal of the Royal Statistical Society
  RECOMMENDATION_5:  Statistica Sinica
  ...
```

### Batch Mode

```
Loaded 100 articles. Starting batch recommendation...
Processing Journal Recommendations: 100%|████████| 100/100
Done! Results saved to: data/results.csv
```

The output CSV will contain the original columns plus 10 additional columns:
`RECOMMENDATION_1`, `RECOMMENDATION_2`, ..., `RECOMMENDATION_10`.

---

## Using the Agent Programmatically

You can also import and use the agent directly in your own script:

```python
from agent import JournalRecommendAgent

agent = JournalRecommendAgent(
    api_key="your-api-key-here",
    scope_csv_path="data/journal_scope.csv"
)

# Single recommendation
result = agent.recommend(
    title="Your paper title",
    abstract="Your abstract here...",
    keywords="keyword1, keyword2, keyword3"
)
for k, v in result.items():
    print(f"{k}: {v}")

# Batch recommendation
import pandas as pd
df = pd.read_csv("data/papers.csv")
df_result = agent.recommend_batch(df)
df_result.to_csv("data/results.csv", index=False)
```

---

## Notes

- The agent sets `temperature=0` by default to ensure stable and reproducible outputs.
- Batch mode uses multithreading (`max_workers=5` by default) to speed up large-scale inference.
- The recommendation is based solely on the provided manuscript information. No external knowledge, web search, or prior publication history is used.
- The candidate journal list is fixed and defined by `journal_scope.csv`.

---

## Citation

If you use this tool in your research, please cite:

```
@article{paper2026,
  title   = {Paper Title},
  author  = {Name},
  journal = {Journal},
  year    = {2026}
}
```

---

## License

This project is licensed under the MIT License.

## Maintenance

The candidate journal list (`data/journal_scope.csv`) will be updated 
periodically to reflect changes in journal scopes and expansions of 
the journal pool. We recommend checking the latest release for the 
most up-to-date version.
