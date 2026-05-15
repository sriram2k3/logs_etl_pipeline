# Logs ETL Pipeline

This project implements a simple yet robust ETL (Extract, Transform, Load) pipeline for processing log files. It is designed to extract log data from either a local file or a remote URL, parse the relevant information, perform a basic analysis, and load the structured data into a MySQL database.

## Features

*   **Dynamic Data Source**: Extracts logs seamlessly from both local file paths and remote URLs.
*   **Log Parsing**: Transforms raw log lines into structured records containing timestamp, status, and IP address.
*   **Data Analysis**: Includes functionality to identify and rank the most frequently blocked IP addresses.
*   **Database Loading**: Loads the processed log data into a MySQL database table for persistent storage and further querying.
*   **Object-Oriented Design**: Utilizes Python classes for modularity and extensibility, separating concerns for data extraction, transformation, and loading.

## How It Works

The ETL process is orchestrated by `main.py` and follows these steps:

1.  **Source Detection**: The script first determines if the `SOURCE_PATH` provided in the `.env` file is a file path or a URL using the `urlcheck.py` utility.
2.  **Extract**: Based on the source type, it instantiates either a `FileLogSource` or `UrlLogSource` object to fetch log data line-by-line.
3.  **Transform**: Each log line is passed to a `LogRecord` object, which parses the line to extract the timestamp, status (e.g., "Block", "Release"), and a valid IP address.
4.  **Collect & Analyze**: The parsed `LogRecord` objects are added to a `Collection` instance. This class holds the data in memory and provides methods for analysis, such as `top_blocked_ips()`. The top 5 blocked IPs are printed to the console.
5.  **Load**: A `DbLoader` object establishes a connection to the MySQL database (using credentials from the `.env` file) and executes a bulk insert to load all the collected log records into the `logs` table.
6.  **Automation**: Using `Windows Task Scheduler` created a scheduled flow to run the main script in a daily basis.
## Prerequisites

*   Python 3.x
*   A running MySQL server instance.

## Setup and Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/sriram2k3/logs_etl_pipeline.git
    cd logs_etl_pipeline
    ```

2.  **Install the required Python packages:**
    ```sh
    pip install requests mysql-connector-python python-dotenv
    ```

3.  **Set up the database:**
    a. Create a new database in your MySQL server.
    b. Execute the following SQL command from `sqltable.sql` to create the target table:
    ```sql
    CREATE TABLE logs (
        timestamp_ DATETIME,
        status_ VARCHAR(10),
        ip_address VARCHAR(25)
    );
    ```

4.  **Configure environment variables:**
    Create a file named `.env` in the root directory of the project and add your configuration details. Use the example below as a template.

    *Example `.env` file:*
    ```env
    # For a local file source
    SOURCE_PATH=ips.txt

    # For a remote URL source (uncomment to use)
    # SOURCE_PATH=http://example.com/path/to/logs.txt

    # Database credentials
    DB_HOST=localhost
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_DATABASE=your_db_name
    ```

## Usage

Once the setup is complete, run the main script from the terminal:

```sh
python main.py
```

The script will print status messages to the console, including the source type, data processing status, the top 5 blocked IPs, and a final confirmation upon successfully loading the data into the database.

## File Descriptions

*   `main.py`: The main entry point for the application. It orchestrates the entire ETL pipeline.
*   `Classes.py`: Contains all the core classes for the pipeline:
    *   `LogSource` / `FileLogSource` / `UrlLogSource`: Handle data extraction.
    *   `LogRecord`: Manages the parsing and structure of a single log entry.
    *   `Collection`: A container for `LogRecord` objects and analysis methods.
    *   `DbLoader`: Manages the database connection and data loading.
*   `urlcheck.py`: A helper script to differentiate between a file path and a URL.
*   `sqltable.sql`: The SQL schema required to create the `logs` table in MySQL.
*   `ips.txt`: A sample log file that can be used as a data source.
