# Import required libraries
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from datetime import datetime
import time


class DataStreamSimulator:
    """Simulates a real-time data stream with patterns, seasonality, and anomalies"""
    
    # constructor to set the seasonal pattern and noise level along with the time index
    # time index is used to emulate the passage of time
    def __init__(self, seasonal_pattern='daily', noise_level=0.1):
        self.seasonal_pattern = seasonal_pattern
        self.noise_level = noise_level
        self.time_index = 0
        
    # this function generates the baseline value based on the seasonal pattern
    # this can be further expanded to include other seasonal patterns
    def _generate_baseline(self):
        """Generate baseline value based on seasonal pattern"""
        if self.seasonal_pattern == 'daily':
            # 24-hour pattern
            hour = self.time_index % 24
            return 10 + 5 * np.sin(2 * np.pi * hour / 24)
        return 10  # Default baseline
    
    # emulates a real time data stream, occasionally returning anomalies
    def get_next_value(self):
        """Generate next value in the stream"""
        try:
            baseline = self._generate_baseline()
            noise = np.random.normal(0, self.noise_level)
            
            # Occasionally inject anomalies (1% chance)
            # could change this to not create spikes for the first hundred values because that affects the mean value a bit
            # which causes less anomalies to occur, because the mean is affected if there are spikes in historical data
            if np.random.random() < 0.01:
                anomaly = np.random.choice([
                    baseline * 3,  # Spike
                    baseline * 0.1,  # Drop
                    baseline + np.random.normal(0, baseline)  # Random deviation
                ])
                self.time_index += 1
                return anomaly
            
            self.time_index += 1
            return baseline + noise
        except Exception as e:
            print(f"Error generating data: {e}")
            return None


class AnomalyDetector:
    """Detects anomalies in real-time data stream"""
    
    def __init__(self, window_size=10, threshold=3):
        self.window_size = window_size
        self.threshold = threshold
        # Circular buffer to store the values
        self.values = deque(maxlen=window_size)
        # Exponentially weighted moving average (EWMA) and EWMA standard deviation
        self.ewma = None
        self.ewma_std = None
        self.alpha = 0.1  # EWMA smoothing factor

    # this function updates the average along with the standard deviation
    def update_stats(self, value):
        """Update EWMA statistics with new value"""
        try:
            if self.ewma is None:
                self.ewma = value
                self.ewma_std = 0
            else:
                # Update EWMA
                self.ewma = self.alpha * value + (1 - self.alpha) * self.ewma
                
                # Update EWMA of squared deviations
                deviation = abs(value - self.ewma)
                self.ewma_std = self.alpha * deviation + (1 - self.alpha) * self.ewma_std
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    def is_anomaly(self, value):
        """Determine if a value is anomalous"""
        try:
            self.values.append(value) # storing historical data
            self.update_stats(value)
            
            if len(self.values) < self.window_size:
                return False
            
            # Check if value deviates significantly from EWMA
            z_score = abs(value - self.ewma) / (self.ewma_std + 1e-10)
            return z_score > self.threshold
        except Exception as e:
            print(f"Error detecting anomaly: {e}")
            return False


# this class helps visualize the data stream and the anomalies using matplotlib
class StreamVisualizer:
    """Real-time visualization of data stream and anomalies"""
    
    def __init__(self, history_size=1000):
        self.history_size = history_size
        self.timestamps = deque(maxlen=history_size)
        self.values = deque(maxlen=history_size)
        # storing x and y coordinates of the anomalies
        self.anomalies_x = deque(maxlen=history_size) # this stores the timestamps of the anomalies
        self.anomalies_y = deque(maxlen=history_size) # this stores the values of the anomalies
        
        # Setup plot
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.line, = self.ax.plot([], [], 'b-', label='Data Stream')
        self.anomaly_scatter = self.ax.scatter([], [], color='red', label='Anomalies')
        self.ax.legend()
        self.ax.set_title('Real-time Data Stream Anomaly Detection')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        
    def update(self, timestamp, value, is_anomaly):
        """Update visualization with new data point"""
        try:
            self.timestamps.append(timestamp)
            self.values.append(value)
            
            if is_anomaly:
                self.anomalies_x.append(timestamp)
                self.anomalies_y.append(value)
            
            # Update plot
            self.line.set_data(list(self.timestamps), list(self.values))
            self.anomaly_scatter.set_offsets(np.c_[list(self.anomalies_x), 
                                                 list(self.anomalies_y)])
            
            # Adjust plot limits
            self.ax.relim()
            self.ax.autoscale_view()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        except Exception as e:
            print(f"Error updating visualization: {e}")


def main():
    """Main function to run the anomaly detection system"""
    
    # Initialize components
    simulator = DataStreamSimulator(seasonal_pattern='daily', noise_level=0.2)
    detector = AnomalyDetector(window_size=100, threshold=3)
    visualizer = StreamVisualizer(history_size=500)
    
    try:
        while True:
            # Generate new value
            value = simulator.get_next_value()
            
            if value is None:  # If there was an error in generating the value, skip the iteration
                continue
                
            timestamp = datetime.now()
            
            # Detect anomalies
            is_anomaly = detector.is_anomaly(value)
            
            # Update visualization
            visualizer.update(timestamp, value, is_anomaly)
            
            # Control update rate
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Stopping data stream...")
        plt.close()
    except Exception as e:
        print(f"Error in main loop: {e}")
        plt.close()

if __name__ == "__main__":
    main()
