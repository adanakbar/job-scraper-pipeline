import pandas as pd


def transform_jobs():
    df = pd.read_csv("raw_jobs.csv")

    # Drop duplicates based on job link
    df.drop_duplicates(subset=["job_link"], inplace=True)

    # Ensure 'company' is string before using .str
    df["company"] = df["company"].astype(str).str.strip().str.title()

    # Ensure 'location' and 'job_title' are strings
    df["location"] = df["location"].astype(str).str.strip()
    df["job_title"] = df["job_title"].astype(str).str.strip()

    # Handle skills column if it exists
    if "skills" in df.columns:
        df["skills"] = df["skills"].astype(str).str.lower().str.replace("\n", " ")

    # Save cleaned data
    df.to_csv("clean_jobs.csv", index=False)
    print("Transform complete. Total jobs:", len(df))
    return df


if __name__ == "__main__":
    transform_jobs()
