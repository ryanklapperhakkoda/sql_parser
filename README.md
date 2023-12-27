
# SQL Query Parser Application

## Overview
This project consists of a Streamlit-based web application designed to parse SQL queries. It includes two main Python files: `main.py` and `parse_tools.py`. The `main.py` file is responsible for the web interface and user interaction, while `parse_tools.py` contains utility functions for parsing and processing SQL queries.

## Installation
To install and run this application, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   ```

2. **Navigate to the project directory:**
   ```bash
   cd [project-directory]
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command in the project directory:

```bash
streamlit run main.py
```

This will start the Streamlit server, and the application should be accessible through a web browser at `localhost:8501`.

## Features
- **SQL Query Input**: Users can input SQL queries for parsing.
- **Query Parsing**: The application parses the SQL query and displays various components such as SELECT, FROM, WHERE clauses.
- **User Feedback**: Users can provide feedback on the accuracy of the parsed query and then send that to a Snowflake table for analysis.

## Files Description
- `main.py`: The main script that runs the Streamlit application, handling user inputs and displaying results.
- `parse_tools.py`: Contains functions for parsing SQL queries and other utility functions used by `main.py`.

## Contributing
Contributions to this project are welcome. Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and commit them.
4. Push to your branch and open a pull request.
