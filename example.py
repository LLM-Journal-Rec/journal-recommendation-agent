import pandas as pd
from agent import JournalRecommendAgent

# ------------------------------------------------------------------ #
#  Configuration
# ------------------------------------------------------------------ #
print("=" * 50)
print("   Journal Recommendation Agent")
print("=" * 50)

API_KEY = input("Enter your API key: ").strip()
BASE_URL = input("Enter API base URL (press Enter for DeepSeek default): ").strip()
if not BASE_URL:
    BASE_URL = "https://api.deepseek.com/v1"

SCOPE_CSV_PATH = "data/journal_scope.csv"

# ------------------------------------------------------------------ #
#  Initialize Agent
# ------------------------------------------------------------------ #
agent = JournalRecommendAgent(
    api_key=API_KEY,
    scope_csv_path=SCOPE_CSV_PATH,
    base_url=BASE_URL
)

# ------------------------------------------------------------------ #
#  Select Mode
# ------------------------------------------------------------------ #
print("\nPlease select a mode:")
print("  [1] Single article recommendation")
print("  [2] Batch recommendation (from CSV)")
print("=" * 50)

mode = input("Enter 1 or 2: ").strip()

# ------------------------------------------------------------------ #
#  Single Recommendation
# ------------------------------------------------------------------ #
if mode == "1":
    print("\n--- Single Article Recommendation ---")
    title    = input("Enter paper title: ").strip()
    abstract = input("Enter abstract: ").strip()
    keywords = input("Enter keywords: ").strip()

    print("\nRunning recommendation, please wait...\n")
    result = agent.recommend(title=title, abstract=abstract, keywords=keywords)

    if result:
        print("Top-10 Recommended Journals:")
        print("-" * 40)
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        print("No result returned. Please check your API key or input.")

# ------------------------------------------------------------------ #
#  Batch Recommendation
# ------------------------------------------------------------------ #
elif mode == "2":
    print("\n--- Batch Recommendation ---")
    input_path  = input("Enter path to input CSV (e.g. data/papers.csv): ").strip()
    output_path = input("Enter path to save output CSV (e.g. data/results.csv): ").strip()

    print("\nLoading data...")
    try:
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} articles. Starting batch recommendation...\n")
        df_result = agent.recommend_batch(df)
        df_result.to_csv(output_path, index=False)
        print(f"\nDone! Results saved to: {output_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
    except ValueError as e:
        print(f"Error: {e}")

# ------------------------------------------------------------------ #
#  Invalid Input
# ------------------------------------------------------------------ #
else:
    print("Invalid input. Please enter 1 or 2.")