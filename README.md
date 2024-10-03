# Efficient Data Stream Anomaly Detection

## Project Description

This project is a Python-based solution for real-time anomaly detection in continuous data streams. The script simulates a data stream with regular patterns, seasonal variations, and random noise, which can represent real-world metrics such as financial transactions, system health data, or IOT sensor readings. The anomaly detection mechanism flags unusual deviations from normal behavior and visualizes the results in real-time.

## Objectives Covered

1. **Algorithm Selection**: The anomaly detection is based on an **Exponentially Weighted Moving Average (EWMA)** algorithm with a Z-score based thresholding mechanism. This method adapts to concept drift and handles seasonal variations effectively, making it suitable for real-time anomaly detection.
2. **Data Stream Simulation**: A custom `DataStreamSimulator` class emulates a data stream with patterns such as daily seasonality, along with random noise. Occasionally, anomalies are injected to simulate real-world deviations.
3. **Anomaly Detection**: The `AnomalyDetector` class detects anomalies in the stream using a sliding window approach. It maintains a history of values and computes both the EWMA and EWMA standard deviation to flag values that deviate significantly from the expected range.
4. **Optimization**: The system is optimized to handle real-time data streams using efficient data structures (like circular buffers) and an adaptive algorithm that minimizes computational overhead while maintaining accuracy.
5. **Visualization**: A `StreamVisualizer` class provides real-time visualization of the data stream and anomalies using `matplotlib`. Anomalous data points are highlighted in red to clearly indicate deviations from the norm.

## Project Structure

- **DataStreamSimulator:**
  Simulates a real-time data stream with seasonal patterns (e.g., daily seasonality) and random noise. The simulator injects occasional anomalies such as spikes, drops, or random deviations. The spikes and drops are controlled by a probability of 0.01, which can be adjusted to change the frequency of anomalies.

- **AnomalyDetector:**
  Detects anomalies in the data stream using an EWMA algorithm with a Z-score threshold. The EWMA is updated with each new value, and the standard deviation is computed using the EWMA. The threshold is set to 3 by default, but can be adjusted to control the sensitivity of the detector.

- **StreamVisualizer:**
  Provides real-time visualization of the data stream and anomalies using `matplotlib`. The visualizer updates the plot with new data points and highlights anomalous values in red for easy identification.

### Key Algorithm Details:

The anomaly detection algorithm uses Exponentially Weighted Moving Average (EWMA) to compute a smoothed average of the incoming data. The EWMA adjusts to new data points using a smoothing factor (alpha), which controls how quickly the model adapts to changes in the data stream. The standard deviation is also computed using EWMA, and anomalies are flagged if the absolute deviation from the average exceeds a Z-score threshold.

- **EWMA:**
  The EWMA is computed as a weighted average of the current value and the previous EWMA value. The weight (alpha) determines how quickly the EWMA adapts to changes in the data stream. A higher alpha value results in a slower adaptation, while a lower alpha value leads to faster adaptation.

  \[
  \text{EWMA}_t = \alpha \cdot \text{Value}\_t + (1 - \alpha) \cdot \text{EWMA}_{t-1}
  \]

- **Z-score for anomaly detection:**

  The Z-score is calculated as the absolute deviation from the EWMA divided by the EWMA standard deviation. A higher Z-score indicates a deviation from the expected behavior, while a lower Z-score indicates a deviation that is within the expected range.

  \[
  Z = \frac{|\text{Value} - \text{EWMA}|}{\text{EWMA Std} + \epsilon}
  \]

- **EWMA Standard Deviation:**

  The EWMA standard deviation is computed using the EWMA of squared deviations. The squared deviation is calculated as the difference between the current value and the EWMA, squared, and the EWMA of squared deviations is updated using the same smoothing factor.

  $$EWMA\_STD(t) = \alpha * deviation + (1 - \alpha) * EWMA\_STD(t-1)$$

  The Z-score threshold is set to 3 by default, but can be adjusted to control the sensitivity of the detector. A higher threshold leads to more anomalies being flagged, while a lower threshold results in fewer anomalies.

## How to Run the Project

To run the project, follow these steps:

1. Clone the repository (or download the zip file):

```bash
git clone https://github.com/Elee-Lawleit/Efficient-Data-Stream-Anomaly-Detection.git
```

2. Navigate to the project directory:

```bash
cd Efficient-Data-Stream-Anomaly-Detection
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the script:

```bash
python anomaly-detector.py
```

The script will start the simulation and visualize the data stream and anomalies in real-time. All the classes and functions are defined in the `anomaly-detector.py` file for easy reference.

## Project Implementation

The project is implemented using Python 3.x and the following libraries:

- NumPy: For numerical computations and data manipulation.
- Matplotlib: For real-time visualization of the data stream and anomalies.
- Deque: For efficient data storage and manipulation.

## Design Decisions

1. **Algorithm Selection:**
   The decision to use an exponentially weighted moving average (EWMA) was based on its efficiency in detecting anomalies in time-series data with seasonality. EWMA adapts to changes quickly while smoothing out noise, and the Z-score calculation provides a robust mechanism for detecting outliers.
2. **Real-time Visualization:**
   The choice of real-time visualization was made to provide immediate feedback to the user. Matplotlib's interactive mode allows for real-time updates, making it easy to visualize the data stream and anomalies as they occur.
3. **Data Structures:**
   Circular buffers are used to store the data stream and anomalies, allowing for efficient handling of the data. The deque data structure is used to maintain the history of values and compute the EWMA and EWMA standard deviation.
4. **Window Size and Threshold:**
   The anomaly detection threshold (Z-score threshold) and the sliding window size were tuned to balance sensitivity and specificity, ensuring the system effectively captures significant deviations while avoiding false positives for this small scale script.
5. **Spikes and Drops in the first 100 values:**
   To simulate the passage of time and the impact of seasonal patterns, the script injects spikes and drops in the first 100 values. This can be changed to not include spikes in the first 100 values, which can affect the mean value and reduce the number of anomalies.

## Limitations and Future Work

- The EWMA algorithm may not be suitable for all data streams, especially those with high-frequency or irregular patterns. Other algorithms like moving averages or median filters could be explored for more robust anomaly detection.
- The choice of seasonal patterns and noise levels could be further optimized for different data streams, especially those with high-frequency or irregular patterns.
- The EWMA algorithm assumes a fixed window size, which may not be suitable for all data streams. Other algorithms like sliding windows or adaptive algorithms could be explored for more flexible and adaptive anomaly detection.
- The EWMA algorithm assumes a _fixed threshold_, which may not be suitable for all data streams. Furthermore, more seasonal patterns or noise levels could be added to the simulation to further test the EWMA algorithm's sensitivity.

## Conclusion

This project demonstrates the effectiveness of an EWMA algorithm for real-time anomaly detection in continuous data streams. The script simulates a data stream with regular patterns, seasonal variations, and random noise, which can represent real-world metrics such as financial transactions, system health data, or IOT sensor readings. The anomaly detection mechanism flags unusual deviations from normal behavior and visualizes the results in real-time. The project is a practical demonstration of the EWMA algorithm and its application in real-world scenarios.
