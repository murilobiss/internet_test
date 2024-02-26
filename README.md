# Internet Speed Test

This Python script performs periodic internet speed tests using the `speedtest-cli` library and plots the results over time. It saves the results to a CSV file and updates the graph every 9 minutes (3 readings) with the new data.

## Features
- Measures download and upload speeds in megabytes per second (MB/s).
- Records ping (latency) in milliseconds (ms).
- Displays the current date and time, along with the speed test results, during each test.
- Generates a graph showing the evolution of download speed, upload speed, and ping over time.
- Calculates and displays the average speed for each metric on the graph.
- Saves the speed test data to a CSV file for further analysis.

## Dependencies
- `speedtest-cli`: Python library for performing internet speed tests.
- `pandas`: Data manipulation library for handling the speed test data.
- `numpy`: Library for numerical operations used to calculate averages.
- `matplotlib`: Library for creating plots to visualize the speed test results.
- `pytz`: Library for working with time zones to ensure correct timestamps.

## Usage
1. Run the script in a Python environment.
2. The script will perform a speed test every 3 minutes and update the graph with the new data.
3. Press `Ctrl + C` to stop the script.

## Note
- The script uses the time zone `America/Sao_Paulo` (GMT-3) to timestamp the speed test data.
- Ensure that the required libraries are installed before running the script.
