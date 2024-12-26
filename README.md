<p align="center">
  <a href="" rel="noopener">
 <img width=300px height=200px src="./assets_readme/globant_logo.png" alt="Project logo"></a>
</p>

<h3 align="center">Globant's Data Engineering Coding Challenge</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success)]()
[![Language](https://img.shields.io/badge/language-python-blue)]()
[![Framework](https://img.shields.io/badge/framework-fastapi-brightgreen)]()
[![Database](https://img.shields.io/badge/database-postgresql-blue)]()
[![Developer](https://img.shields.io/badge/Developer-Sebastián_Martínez-orange)]()

</div>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🚀 Project Overview ](#-project-overview-)
- [🔧 Prerequisites ](#-prerequisites-)
- [📡 API Endpoints ](#-api-endpoints-)
  - [CSV Upload Endpoint](#csv-upload-endpoint)
  - [Reporting Endpoints](#reporting-endpoints)
- [🗂️ Project Structure ](#️-project-structure-)
- [🛠 Installation ](#-installation-)
- [🏃 Running the Application](#-running-the-application)
  - [Using Docker](#using-docker)
  - [Local Development](#local-development)
  - [🧪 Testing](#-testing)
- [📊 Sample Usage](#-sample-usage)
- [📝 Notes](#-notes)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🧐 About <a name = "about"></a>

This is a coding challenge for Globant's Data Engineering position. The challenge consists of creating an API that reads data from a CSV file, processes it and stores it in a database. The data is related to the sales of a company and the goal is to create a database that allows to query the data in a more efficient way.

The API is built using FastAPI and the database is PostgreSQL. The API has the following endpoints:

- `/upload/csv/{model}`: This endpoint receives a CSV file and a model name. The model name is used to determine the structure of the data in the CSV file. The data is processed and stored in the database. The model name can be one of the following:
  - `departments`: The CSV file contains the following columns: `department_id`, `department_name`.
  - `jobs`: The CSV file contains the following columns: `job_id`, `job_title`.
  - `employees`: The CSV file contains the following columns: `employee_id`, `employee_name`, `hired_time`, `department_id`, `job_id`.

- `/reports/hires/departments/q/{year}`: Number of employees hired for each job and department in the given year divided by quarter. The table must be ordered alphabetically by department and job.

- `/reports/hires/departments/mean/{year}`: List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in the given year for all the departments, ordered by the number of employees hired (descending).

## 🚀 Project Overview <a name = "project_overview"></a>

The project is a data processing API that:
- Reads and uploads CSV files for departments, jobs, and employees
- Provides analytical reports on employee hiring
- Demonstrates efficient data transformation and storage techniques

## 🔧 Prerequisites <a name = "getting_started"></a>

Before you begin, ensure you have:
- Python 3.11+
- Docker
- Docker Compose
- pip package manager

## 📡 API Endpoints <a name = "api_endpoints"></a>

### CSV Upload Endpoint
`/upload/csv/{model}`
- Supported models:
  * `departments`: Upload department data
  * `jobs`: Upload job data
  * `employees`: Upload employee data

### Reporting Endpoints
1. `/reports/hires/departments/q/{year}`
   - Provides employee hiring count by job and department per quarter
   - Ordered alphabetically by department and job

2. `/reports/hires/departments/mean/{year}`
   - Lists departments that hired more employees than the annual mean
   - Ordered by number of employees hired (descending)

## 🗂️ Project Structure <a name = "project_structure"></a>
```
globant-data-eng/
│ ├── src/ # Source code
│ ├── main.py # FastAPI application
│ ├── models/ # Database models
│ ├── schemas/ # Pydantic schemas
│ └── services/ # Business logic
├── data/ # CSV data files
├── tests/ # Unit and integration tests
├── docker-compose.yml # Docker configuration
└── requirements.txt # Python dependencies
```

## 🛠 Installation <a name = "installation"></a>

1. Clone the repository
```bash
git clone https://github.com/your-username/globant-data-eng.git
cd globant-data-eng
```
2. Create virtual environment
```bash
uv venv --python 3.12
source venv/bin/activate
```

3. Install dependencies
```bash
uv pip install -r requirements.txt
```

## 🏃 Running the Application

### Using Docker
```bash
docker-compose up --build
```
### Local Development
```bash
uvicorn src.main:app --reload
```
### 🧪 Testing
Run tests using pytest:

```bash
pytest tests/
```
## 📊 Sample Usage

1. Upload Departments CSV
```bash
curl -X POST /upload/csv/departments -F "file=@departments.csv"
```
2. Get Hiring Report
```bash
curl /reports/hires/departments/q/2021
```

## 📝 Notes

* Ensure CSV files match the specified column structures
* Use appropriate error handling when uploading files
* Check Docker and network configurations if experiencing connection issues

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License
This project is open-source. Please check the LICENSE file for details.