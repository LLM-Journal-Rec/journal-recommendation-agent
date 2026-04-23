import re
import pandas as pd
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from prompt import construct_prompt


class JournalRecommendAgent:
    def __init__(self, api_key, scope_csv_path,
                 base_url="https://api.deepseek.com/v1",
                 model="deepseek-chat",
                 max_workers=5):
        """
        Args:
            api_key:        Your API key
            scope_csv_path: Path to journal_scope.csv (columns: Journal, Scope)
            base_url:       API base URL
            model:          Model name
            max_workers:    Number of parallel threads for batch inference
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.max_workers = max_workers
        self.scope_df = self._load_scope(scope_csv_path)
        self.journal_scope, self.journal_options = self._build_scope_text()

    # ------------------------------------------------------------------ #
    #  Data loading
    # ------------------------------------------------------------------ #
    def _load_scope(self, path):
        df = pd.read_csv(path, encoding="utf-8-sig")
        assert "Journal" in df.columns and "Scope" in df.columns, \
            "CSV must contain 'Journal' and 'Scope' columns."
        return df

    def _build_scope_text(self):
        journal_scope = "Here is a brief summary of the journal scopes:\n\n"
        for i, row in enumerate(self.scope_df.itertuples(), 1):
            journal_scope += f"{i}. {row.Journal} — {row.Scope.strip()}\n"

        journal_list = self.scope_df["Journal"].dropna().unique().tolist()
        journal_options = "\n".join(
            [f"{i+1}. {name}" for i, name in enumerate(journal_list)]
        )
        return journal_scope, journal_options

    # ------------------------------------------------------------------ #
    #  Single inference
    # ------------------------------------------------------------------ #
    def _call_api(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return completion.choices[0].message.content.strip()

    def _parse_response(self, response):
        result = {}
        for line in response.splitlines():
            match = re.match(r"RECOMMENDATION_(\d+):\s*(.+)", line.strip(), re.IGNORECASE)
            if match:
                result[f"RECOMMENDATION_{match.group(1)}"] = match.group(2).strip()
        return result

    def recommend(self, title, abstract, keywords):
        """
        Single-article recommendation.

        Returns:
            dict: {"RECOMMENDATION_1": "...", ..., "RECOMMENDATION_10": "..."}
        """
        prompt = construct_prompt(
            title, abstract, keywords,
            self.journal_scope, self.journal_options
        )
        try:
            response = self._call_api(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"API error: {e}")
            return {}

    # ------------------------------------------------------------------ #
    #  Batch inference
    # ------------------------------------------------------------------ #
    def _process_row(self, idx, row):
        try:
            result = self.recommend(
                title=row["title"],
                abstract=row["abstract"],
                keywords=row["keywords"]
            )
            return idx, result
        except Exception as e:
            print(f"Error at index {idx}: {e}")
            return idx, None

    def recommend_batch(self, df):
        """
        Batch recommendation for a DataFrame.

        Args:
            df: DataFrame with columns [title, abstract, keywords]

        Returns:
            DataFrame with RECOMMENDATION_1 ~ RECOMMENDATION_10 columns appended
        """
        df = df.copy()
        for i in range(1, 11):
            df[f"RECOMMENDATION_{i}"] = None

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_row, idx, row): idx
                for idx, row in df.iterrows()
            }
            for future in tqdm(as_completed(futures), total=len(futures),
                               desc="Processing Journal Recommendations"):
                idx, result = future.result()
                if result:
                    for i in range(1, 11):
                        df.at[idx, f"RECOMMENDATION_{i}"] = result.get(
                            f"RECOMMENDATION_{i}", None
                        )
        return df