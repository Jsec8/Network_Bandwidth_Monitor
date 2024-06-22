# Bandwidth Monitor

This project is a bandwidth monitor written in Python that allows users to visualize network usage in real-time in terms of bytes sent and received per second. It also allows setting thresholds to generate alerts when certain bandwidth limits are exceeded.

## Features

- Real-time monitoring of bandwidth usage.
- Interactive graphs to visualize network usage.
- Data logging in a CSV file.
- Threshold settings for bandwidth alerts.
- User-friendly graphical interface with Tkinter.

## Requirements

To run this project, you need to have the following requirements installed:

- Python 3.6 or higher
- The following Python libraries:
  - psutil
  - tkinter
  - matplotlib

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Jsec8/network_bandwidth_monitor.git
    cd network_bandwidth_monitor
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install psutil matplotlib
    ```

## Usage

To start the bandwidth monitor, run the following command:

```bash
python bandwidth_monitor.py

## Graphical Interface

Upon starting the program, a window will open with a real-time graph of bandwidth usage.
You can set thresholds for bytes sent and received using the corresponding input fields and clicking the "Set Thresholds" button.
If any of the set thresholds are exceeded, an alert will be generated in the interface.
To stop the monitoring, click the "Stop Monitoring" button.

## CSV File

The bandwidth data is logged in the bandwidth_data.csv file located in the project directory.

## Contributing

Contributions are welcome. If you wish to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/new-feature).
Make your changes and commit them (git commit -am 'Add new feature').
Push your changes to the branch (git push origin feature/new-feature).
Open a Pull Request.