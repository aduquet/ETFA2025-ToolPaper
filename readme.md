# From Testing to Insights: A Tool for Automating the Ranking and Analysis of PID Simulation Test Runs

 The project focuses on exploring simulation scenarios across various machine configurations, providing insights into parameter tuning, system behavior, and performance evaluation.

---
# Screencast

https://youtu.be/X-kMTkl8oaQ
___

## Features

- **Simulation Analysis**: Tools to simulate and analyze PID controllers under multiple configurations.
- **Data Visualization**: Interactive plots for exploring system performance metrics.
- **Ranking System**: Automated ranking of test scenarios based on predefined metrics.

---

## Requirements

- **Python Version**: 3.11.7 (managed via `pyenv` or another version manager)
- **Dependency Manager**: [Poetry](https://python-poetry.org/)

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aduquet/ETFA2025-ToolPaper.git
cd ETFA2025-ToolPaper
```

### 2. Install Dependencies
Ensure you have Poetry installed. Then, run:
```bash
poetry install
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```plaintext
FIREBASE_CREDENTIALS={"type":"service_account", ...}
```
Alternatively, save the credentials in a `firebase_credentials.json` file and update the `.env` file:
```plaintext
FIREBASE_CREDENTIALS_PATH=firebase_credentials.json
```

---

## Usage

### Run the Application
Start the application using:
```bash
poetry run python app_fb.py
```

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t pid-controller-app .
   ```

2. Run the container:
   ```bash
   docker run -it --rm -p 5006:5006 --env-file .env --name pid-controller pid-controller-app
   ```

---

## Project Structure

```
.
├── app_fb.py                  # Main application entry point
├── constants.py               # Constants used across the project
├── get_metrics_fb.py          # Metric calculations
├── plot_handler_hv.py         # Plotting and visualization utilities
├── ranking_system.py          # Ranking logic for test cases
├── signal_metrics.py          # Signal processing utilities
├── pyproject.toml             # Project dependencies and settings
├── Dockerfile                 # Docker setup
├── README.md                  # Project documentation
├── .env                       # Environment variables (excluded from Git)
```

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request. Ensure that your code follows the project's style guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Special thanks to the industrial partners for providing insights and support for the dataset and simulation scenarios.
```

