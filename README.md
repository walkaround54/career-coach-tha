# career-coach-tha | Hsu Stanley

## Setup Guide

1. Download `tha_stan.zip` from this repo and extract its contents.
2. If you have Python installed, proceed to **Step 4**.
3. If you **do not** have Python installed, follow the instructions below:

**For Mac Users**:

- **a.** Check if Python 3 is installed by opening **Terminal** and running:
  ```sh
  python3 --version
  ```
  - If Python is installed, you will see output similar to:
    ```
    Python 3.x.x
    ```
- **b.** If Python is **not installed**, install it using:
  ```sh
  brew install python
  ```

**For Windows Users**:

- **a.** Download the latest **Stable Release** from **[python.org](https://www.python.org/downloads/windows/)**.
- **b.** Run the installer and **check the box** `"Add Python to PATH"` before clicking **Install**.
- **c.** Verify your installation by opening **Command Prompt** and running:
  ```sh
  python --version
  ```
  - If Python is installed, you will see output similar to:
    ```
    Python 3.x.x
    ```

4. Once Python is installed, open **Terminal** (Mac) or **Command Prompt** (Windows) and navigate to the location of the extracted `tha_stan` folder using:

   ```sh
   cd "replace with path to tha_stan folder"

   ```

5. Create a new virtual environment for this project using:

```sh
python3 -m venv venv
```

6. Activate the virtual environment.

For Mac Users

```sh
source venv/bin/activate
```

For Windows Users

```sh
venv\Scripts\activate
```

7. Install Dependencies using

```sh
pip install -r requirements.txt
```

## Case Study Scenario 1

### Running Scenario 1 Application

Please ensure you are in the tha_stan directory in command shell or Terminal. Navigate to the scenario_1 directory using the following command:

```sh
cd scenario_1
```

Once Python, virtual environment and dependencies have been set up, run the app using the following command:

```sh
python main.py
```

This will complete each step required in the pipeline. Upon completion of the pipeline, you should see

```sh
Scenario 1 Pipeline Completed
```

To run individual modules, use the following command:

```sh
python (change module name).py
```

### **Architecture Diagram**

![Scenario 1 Architecture Diagram](readme_images/scenario_1_architecture.jpg)

**Scenario 1's Architecture consists of 4 layers:**

1. Raw Data Layer

- Contains unprocessed Zomato Restaurant Data and Country Excel Data

2. Preprocessing Layer

- Contains Preprocessing Module that reads raw data and writes relevant data to csv file

3. Extraction and Data Manipulation Layer

- Extraction Module 1, Extraction Module 2 and Analysis Module extract and manipulate preprocessed data

4. Output Layer

- Contains files generated from extraction and data manipulation layer

**Why have a preprocessing module?**
Upon creating and using the "inspect_json" function (now found in preprocessing_module.py), it is evident that the JSON data structure is messy and difficult to parse.

![Inspect JSON Preview](readme_images/inspect_json_preview.jpg)

**Preview of JSON Structure**

Therefore, for modularity, a preprocessing module was first created to parse the essential JSON data, then proceed with data manipulation, extraction and analysis in extraction module 1 and 2 and the analysis module.

Additional fields to be saved to the "preprocessing_csv" can be included accordingly by editing the "json_to_restaurant_details_csv" function in the preprocessing module.

Duplicate restaurants and events are dropped here, with restaurants requiring an exact match to be dropped since it is possible a restaurant changes cuisine or location over time. For events, only the restaurant id, event name and event date need to match for it to be considered a duplicate entry.

![Drop duplicate events](readme_images/dropping_event_duplicates.jpg)
**Conditions for Events to be considered Duplicate**

### **Potential Architecture Diagram with Cloud Services Integrated**

![Scenario 1 Cloud Architecture](readme_images/scenario_1_cloud_architecture.jpg)

The Updated Architecture with Cloud Services now consists of 5 layers:

1. Raw Data Layer
2. Preprocessing Layer
3. Data Storage/Warehousing Layer (new)
4. Extraction and Data Manipulation Layer
5. Output/Visualization Layer

Assuming the volume and frequency of Data to be ingested and processed is significantly higher, integrating Cloud Services cans make our application highly scalable, available and maintainable.

With cloud services integrated, the **Raw Data** is now stored in a Data Lake, Amazon S3 first. This allows for data from multiple sources and formats to be scalably stored. S3 can be configured to allow for faster but more costly on demand retrieval, if the raw data has to be constantly read from, or configured to be slower access but lower in cost, for archival/large batch processing purposes.

The **Preprocessing Layer** now uses Amazon Glue Crawler to automatically crawl the S3 bucket(s), extract the schema of the raw data and store data into an AWS Glue Data Catalogue. The crawled data can also be converted to more memory efficient formats like Parquet.

In addition, Amazon Glue ETL Jobs can help do initial transformations and mappings for restaurant and event data. These Glue Jobs can be configured to automatically process the data conditionally (like when new raw data is uploaded to S3) for stream processing or processed as a batch less frequently (end of the week/month etc). Apache Airflow DAGs can also be implemented for scheduled Glue Job execution.

There is a new **Data Storage/Warehousing Layer** where preprocessed data is stored in a Data Warehouse. Since we are dealing with tabular data, Amazon Redshift can be utilised as it is buil for columnar storage. The Redshift Data Warehouse allows for efficient data retrieval for manipulation and analysis, with a standardized schema enforced for the preprocessed data.

For the **Extraction and Data Manipulation** layer, since the volume of data is large, instead of using Pandas/Python, Amazon Athena can be used to make efficient SQL queries and extract data from the Data Warehouse, which can then be visualized/analyzed in Amazon Quicksight (**Output Layer**). Big Data frameworks like Apache Spark can also be used for Data Manipulation instead.

### Scenario 1 Task 1

To complete task 1, the preprocessed restaurant data from the preprocessing module is utilised as the data source. "extraction_module_1.py" consists of a "load_country_codes" function and "filter_restaurant_details" function.

The "load_country_codes" that will take an excel path of country code mappings as input and output a dictionary of country code mappings.

The "filter_restaurant_details" will make use of the "load_country_codes" function to take in a country code mapping and preprocessed restaurant data to output only restaurants that have a valid country code mapping. Empty fields are populated with "NA".

The output, "restaurant_details.csv" is stored in the output/task_1 folder.

### Scenario 1 Task 2

Preprocessed event data from the preprocessing module is utilised as the data source. "extraction_module_2.py" consists of a "filter_events_by_date" function.

The "filter_events_by_date" function takes in preprocessed event data, and a date range to filter events by. It will output events that have fall within the given date range.

To handle events with either a valid start or end date, but not both, the following logic was included.
![Event Filter by Date Logic](readme_images/event_filter.jpg)
**Logic to allow permutations of valid start and end date, valid start but invalid end date, valid end but invalid start date**

For this task, the date range is set for dates that fall within April 2019.

The output, "restaurant_events.csv" is stored in the output/task_2 folder.

### Scenario 1 Task 3

Output data from task 1, "restaurant_details.csv" is used as the data source.

"analysis_module.py" reads the restaurant details data, and inspects the unique rating_text values. Since there are rating_texts that are not in English and restaurants that are not rated, the non English ratings would be mapped to either of the "Excellent, Very Good, Good, Average, Poor" categories and entries without ratings would be removed.

![Text Rating Mapping](readme_images/text_rating_mapping.jpg)
**Mapping Non English Text Ratings**

The output, **"ratings_analysis.pdf" is stored in the output/task_3 folder.**

**The following 6 data visualizations were used to analyse and determine rating text thresholds. The insights from each visualization are also listed:**

1. groupby text rating category and describe() to provide summary statistics for the aggregate ratings

- This gave a high level view of the text rating categories. The counts of each category other than poor were sufficient.
- There seemed to be a clear segmentation of text rating by aggregate rating.

2. Histogram of aggregate ratings

- Most ratings seemed to fall within the 4.0 and 4.5 range, leading to a left skew distribution.
- This could indicate that users tend to leave positive reviews, or that restaurants included in the raw JSON tend to be more popular/well received.
- The high concentration of 4.0 and 4.5 ish ratings may lead to difficulties in segmenting Good, Very Good and Excellent Ratings.

3. Bar plot of counts of rating text categories

- There is a disproportionately high number of Very Good ratings compared to Poor, Average and Good ratings.
- Some of the Very Good ratings can likely be shifted to Good or Excellent

4. Scatterplot of mean aggregate rating by rating text

- There is a clear linear trend of the means increasing from Poor to Excellent.
- The means can serve as a relatively reliable reference point for thresholds.

5. Box plot of aggregate ratings by rating text

- Box plot whiskers give a clear visual segmentation of the range of non outliers for the Average to Excellent ratings.

6. Violin plot of ratings for each rating text

- Violin plots clearly indicate visually the rating range in which majority of rating text categories lie.
- Can decide aggregate rating threshold for rating text categories by evaluating aforementioned ranges together with box plot whisker ranges

**Task 3 Analysis Conclusions**

Based on the analysis conducted and primarily looking at the insights from visualization 5 and 6, the following rating text thresholds have been obtained:

- 0.0 <= Poor < 3.0
- 3.0 <= Average < 3.7
- 3.7 <= Good < 4.0
- 4.0 <= Very Good < 4.4
- 4.4 <= Excellent <= 5.0

## Case Study Scenario 2

### **Architecture Diagram**

![Scenario 2 Architecture Diagram](readme_images/scenario_2_architecture.jpg)

**Scenario 2's Architecture consists of the following components:**

1. CLI Module for both Input and Output

- This module contains the information to be displayed on the CLI
- User selection choices and input choices are determined here

2. CSV Processing Module

- This module processes and cleans raw static carpark csv data

3. API Fetcher Module

- This module will fetch Live Carpark API data

4. Merged Data Processing Module

- This module ingests, merges and cleans Live API Data and static processed carpark data

5. User Input Handling Module

- This module will take user input, and validate if it **fuzzily** matches static carpark data first
- If the carpark/location can be fuzzily matched, it calls the API Fetcher Module (module 3) to fetch Live API Data, and then calls Merged Data Procesing Module (module 4) to reprocess the newly fetched Live API Data

**Why use fuzzy matching for validation?**

The "fuzzywuzzy" package allows for fuzzy matching of user inputted data, and provides an approximate match score.

This allows for obviously incorrect addresses or carpark numbers, i.e a string of random gibberish "xcmvnenFFFds" to be filtered away.

Only matches that hit a certain match score i.e 85% match will be displayed, allowing graceful handling of user input errors.

**Why only fetch Live API Data when input validated?**

This prevents excessive API calls that will slow down the application or unnecessarily add to the API retrieval rate limit.

### Scenario 2 Task 1
