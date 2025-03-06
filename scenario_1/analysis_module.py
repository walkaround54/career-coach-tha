import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages

# this module visualizes processed restaurant detail data and saves it to "ratings_analysis.pdf"

# get base directory
BASE_DIR = Path(__file__).resolve().parent

# define input and output directories dynamically
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
OUTPUT_DATA_DIR = BASE_DIR / "output/task_3"


def analyze_ratings(input_csv_path, pdf_output_path):
    """
    creates visualizations using processed restaurant details and saves them to "ratings_analysis.pdf"
    """
    df = pd.read_csv(input_csv_path)

    # list all unique values for rating_text
    print(f'\n Unique rating_text values: \n {df["rating_text"].unique()}')

    # drop "Not rated" values
    df = df[df["rating_text"] != "Not rated"]

    # since there are ratings in other languages, map all ratings to English
    rating_text_mapping = {
        "Bardzo dobrze": "Very Good",
        "Bueno": "Good",
        "Eccellente": "Excellent",
        "Excelente": "Excellent",
        "Muito Bom": "Very Good",
        "Muy Bueno": "Very Good",
        "Skvělá volba": "Very Good",
        "Skvělé": "Excellent",
        "Terbaik": "Excellent",
        "Velmi dobré": "Very Good"
    }
    df["rating_text"] = df["rating_text"].replace(rating_text_mapping)

    # define ordered categories for rating_text
    ordered_classes = ["Poor", "Average", "Good", "Very Good", "Excellent"]
    df["rating_text"] = pd.Categorical(
        df["rating_text"], categories=ordered_classes, ordered=True)

    # convert 'user_aggregate_rating' to numeric
    df["user_aggregate_rating"] = pd.to_numeric(
        df["user_aggregate_rating"], errors="coerce")

    # drop missing values for aggregate ratings
    df = df.dropna(subset=["user_aggregate_rating"])

    # groupby rating_text and describe to get idea of data
    rating_summary = df.groupby("rating_text", observed=False)[
        "user_aggregate_rating"].describe()
    print(f"\nPreliminary Rating Summary:\n {rating_summary}")

    # create figure for summary table
    fig_summary, ax_summary = plt.subplots(figsize=(10, 4))
    ax_summary.axis("tight")
    ax_summary.axis("off")
    ax_summary.set_title(
        "1: Summary Statistics of Aggregate Rating by Rating Text")
    table = ax_summary.table(cellText=rating_summary.round(2).values,
                             colLabels=rating_summary.columns,
                             rowLabels=rating_summary.index,
                             cellLoc="center",
                             loc="center")

    # 1: histogram of aggregate ratings
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.hist(df["user_aggregate_rating"], bins=20,
             color="blue", alpha=0.7, edgecolor="black")
    ax1.set_title("2: Distribution of Aggregate Ratings")
    ax1.set_xlabel("Aggregate Rating", fontweight="bold")
    ax1.set_ylabel("Count", fontweight="bold")

    # 2: bar plot for counts of rating_text
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    rating_counts = df["rating_text"].value_counts()
    rating_counts = rating_counts.reindex(
        ordered_classes, fill_value=0)
    ax2.bar(rating_counts.index, rating_counts.values, color="blue", alpha=0.7)
    ax2.set_title("3: Count of Each Rating Text")
    ax2.set_xlabel("Rating Text", fontweight="bold")
    ax2.set_ylabel("Count", fontweight="bold")
    ax2.set_xticks(range(len(ordered_classes)))
    ax2.set_xticklabels(ordered_classes, rotation=0)

    # 3: bar plot for mean aggregate rating by rating_text
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    mean_ratings = df.groupby("rating_text", observed=False)[
        "user_aggregate_rating"].mean()
    mean_ratings = mean_ratings.reindex(ordered_classes, fill_value=0)

    ax3.scatter(mean_ratings.index, mean_ratings.values,
                color="red", alpha=0.7)

    ax3.set_title("4: Mean Aggregate Rating by Rating Text")
    ax3.set_xlabel("Rating Text", fontweight="bold")
    ax3.set_ylabel("Mean Aggregate Rating", fontweight="bold")
    ax3.set_xticks(range(len(ordered_classes)))
    ax3.set_xticklabels(ordered_classes, rotation=0)
    ax3.set_ylim(2.0, 5.0)

    # Add exact value labels for each data point
    for i, value in enumerate(mean_ratings.values):
        ax3.text(i, value + 0.05, f"{value:.2f}",
                 ha="center", fontsize=10, fontweight="bold")

    # 4: box plots of aggregate ratings by rating_text with mean and whisker labels
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    boxplot = df.boxplot(column="user_aggregate_rating", by="rating_text",
                         ax=ax4, grid=False, patch_artist=True)

    ax4.set_title("5: Box Plot of Aggregate Ratings by Rating Text")
    ax4.set_xlabel("Rating Text", fontweight="bold")
    ax4.set_ylabel("Aggregate Rating", fontweight="bold")
    ax4.set_xticks(range(1, len(ordered_classes) + 1))
    ax4.set_xticklabels(ordered_classes, rotation=0)
    ax4.set_ylim(2.0, 5.0)
    plt.suptitle("")

    # get data for whiskers and mean value labels
    box_data = df.groupby("rating_text", observed=False)[
        "user_aggregate_rating"].describe()

    for i, cat in enumerate(ordered_classes):
        if cat in box_data.index:
            mean_value = box_data.loc[cat, "mean"]
            min_value = box_data.loc[cat, "min"]
            max_value = box_data.loc[cat, "max"]

            # label mean
            ax4.text(i + 1, mean_value + 0.02, f"Mean: {mean_value:.2f}",
                     ha="center", fontsize=7, fontweight="bold", color="blue")

            # label whiskers
            ax4.text(i + 1, min_value - 0.15, f"Min: {min_value:.2f}",
                     ha="center", fontsize=7, fontweight="bold", color="red")
            ax4.text(i + 1, max_value + 0.15, f"Max: {max_value:.2f}",
                     ha="center", fontsize=7, fontweight="bold", color="red")

    # 5: violin plots of aggregate ratings by rating_text
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    df_sorted = df.sort_values("rating_text")
    violin_data = [df_sorted[df_sorted["rating_text"] == cat]
                   ["user_aggregate_rating"].dropna() for cat in ordered_classes]

    parts = ax5.violinplot(violin_data, showmedians=True)

    ax5.set_xticks(range(1, len(ordered_classes) + 1))
    ax5.set_xticklabels(ordered_classes, rotation=0)
    ax5.set_title("6: Violin Plot of Ratings Per Rating Text")
    ax5.set_xlabel("Rating Text", fontweight="bold")
    ax5.set_ylabel("Aggregate Rating", fontweight="bold")
    ax5.set_ylim(2.0, 5.0)

    # save figures onto a pdf
    with PdfPages(pdf_output_path) as pdf:
        pdf.savefig(fig_summary)
        pdf.savefig(fig1)
        pdf.savefig(fig2)
        pdf.savefig(fig3)
        pdf.savefig(fig4)
        pdf.savefig(fig5)

    print(f"\nRating analysis saved at: {pdf_output_path}")


def main():
    """Runs analysis module standalone (for testing)."""
    input_csv_path = PREPROCESSED_DATA_DIR / "preprocessed_restaurant_details.csv"
    pdf_output_path = OUTPUT_DATA_DIR / "ratings_analysis.pdf"

    analyze_ratings(input_csv_path, pdf_output_path)


if __name__ == "__main__":
    main()
