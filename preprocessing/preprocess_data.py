import pandas as pd
import numpy as np

apps_df = pd.read_csv("data/Play Store Data.csv")
reviews_df = pd.read_csv("data/User Reviews.csv")
apps_df.drop_duplicates(subset="App", inplace=True)
apps_df["Rating"] = pd.to_numeric(apps_df["Rating"], errors="coerce")
apps_df["Reviews"] = pd.to_numeric(apps_df["Reviews"], errors="coerce")
apps_df["Size"] = apps_df["Size"].replace("Varies with device", np.nan)
apps_df["Size_MB"] = (
    apps_df["Size"]
    .str.replace("M", "", regex=False)
    .str.replace("k", "", regex=False))
apps_df["Size_MB"] = pd.to_numeric(apps_df["Size_MB"], errors="coerce")
apps_df["Installs"] = (
    apps_df["Installs"]
    .str.replace("+", "", regex=False)
    .str.replace(",", "", regex=False))
apps_df["Installs"] = pd.to_numeric(apps_df["Installs"], errors="coerce")
apps_df["Price"] = (
    apps_df["Price"]
    .str.replace("$", "", regex=False))
apps_df["Price"] = pd.to_numeric(apps_df["Price"], errors="coerce")
apps_df["Last Updated"] = pd.to_datetime(
    apps_df["Last Updated"], errors="coerce")
apps_df["App_Name_Length"] = apps_df["App"].str.len()
reviews_df["Sentiment_Polarity"] = pd.to_numeric(
    reviews_df["Sentiment_Polarity"], errors="coerce")
reviews_df["Sentiment_Subjectivity"] = pd.to_numeric(
    reviews_df["Sentiment_Subjectivity"], errors="coerce")
review_summary = reviews_df.groupby("App").agg(
    Avg_Sentiment_Polarity=("Sentiment_Polarity", "mean"),
    Avg_Sentiment_Subjectivity=("Sentiment_Subjectivity", "mean")).reset_index()
final_df = apps_df.merge(review_summary, on="App", how="left")
final_df.to_csv("data/cleaned_apps.csv", index=False)