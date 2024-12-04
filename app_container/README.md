# ICST2025-ToolPaper


This project provides a set of Python scripts and tools for analyzing and ranking the performance of PID controllers based on simulated data. The tool enables parameter exploration and performance evaluation across multiple machine configurations, such as systems with and without a brake assistant.

## Features

- **Data Normalization**: Normalizes data based on a reference test (`t0`) for better comparative analysis.
- **Performance Metrics**: Calculates key metrics such as pressure and speed energy, oscillations, and response times.
- **Ranking System**: Ranks test cases based on weighted scores and penalties derived from performance metrics.
- **Visualization**: Generates interactive plots for pressure and speed signals using Holoviews and Matplotlib.
- **Simulation Scenarios**: Supports configurations with and without brake assistance for testing parameter robustness.

---

## File Descriptions

### Core Scripts

- **`app_fb.py`**: Main application script that integrates all components and provides an interactive interface for ranking and visualization.
- **`constants.py`**: Contains configuration variables and constants used throughout the project.
- **`get_metrics_fb.py`**: Processes simulation data to calculate key performance metrics such as energy and oscillations.
- **`plot_handler_hv.py`**: Generates interactive plots for visualizing pressure and speed signals.
- **`ranking_system.py`**: Implements the ranking logic for evaluating and comparing test cases.
- **`signal_metrics.py`**: Defines a class for calculating signal-related metrics such as energy and oscillation frequency.

### Configuration Files

- **`Dockerfile`**: Configuration for containerizing the application using Docker.
- **`pyproject.toml`**: Specifies project dependencies and settings.

---

## Dependencies

To run this tool, ensure the following dependencies are installed:

- Python 3.8 or higher
- Libraries:
  - `pandas`
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `holoviews`
  - `panel`
  - `bokeh`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install dependencies as mentioned above.

3. Run the application:

   ```bash
   python app_fb.py
   ```

   This will start a server that provides an interactive interface for exploring and analyzing the simulation data.

4. Open your browser and navigate to the displayed local server address (e.g., `http://localhost:5006/app`).

---

## Instructions for Use

1. Upload your dataset in the expected JSON format.
2. Adjust weights and parameters through the interactive sliders and checkboxes.
3. Explore the visualizations for pressure and speed signals.
4. View the ranked results based on your criteria.
5. Export results or plots as needed.

---

## Dataset Reproducibility

### Configuration Data

- **PID Parameters**: Proportional (\(K_p\)), integral (\(K_i\)), and derivative (\(K_d\)) gains.
- **Brake Assistant**: Boolean flag indicating whether the brake assistant is enabled.
- **Target Signals**: Desired behavior for pressure and speed signals.

### Raw Data

- Time-series outputs of **pressure** and **speed** responses under various configurations.

### Derived Data

- Metrics such as energy, oscillation frequency, rising times, and growth rates are computed to evaluate system performance.

---

## Contributing

Contributions to this project are welcome. Please submit issues or pull requests through the repository.

---

## License

This project is proprietary due to its association with a confidential industrial use case.

---

## Firebase Credentials

This application uses Firebase for authentication. To set up credentials:

### Using a `.env` File
1. Create a `.env` file in the root directory.
2. Add the Firebase credentials as a single JSON string under `FIREBASE_CREDENTIALS`.

### Using a JSON File
1. Save the Firebase credentials as a `firebase_credentials.json` file in the root directory.
2. Ensure the file path matches the one referenced in `app_db.py`.

**Important**: Do not share your credentials publicly. Add `.env` or `firebase_credentials.json` to `.gitignore` to prevent them from being pushed to the repository.

