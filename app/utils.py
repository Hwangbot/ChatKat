from datetime import datetime

def standardize_column_name(name: str) -> str:
    return str(name).strip().lower().replace(" ", "_")

def cast_column_to_float(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
    return df

def parse_date_column(df, col_name, fmt="%Y-%m-%d"):
    df[col_name] = pd.to_datetime(df[col_name], format=fmt, errors="coerce")
    return df

def format_summary_for_prompt(summary_lines):
    return "\n".join(f"- {line}" for line in summary_lines)

import time
def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} executed in {time.time() - start:.2f}s")
        return result
    return wrapper
