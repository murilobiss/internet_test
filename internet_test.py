import time
from datetime import datetime
import speedtest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz

st = speedtest.Speedtest()

# Initialize the lists/variables to store the measured speeds
download = []
upload = []
ping = []
measurement_times = []

# Program interface
print('------------------------------------------------')
print('             Internet Speed Test                ')
print('------------------------------------------------')

# Test execution
try:
    while True:
        # Calculate internet speeds in bytes per second
        download_bytes = st.download()
        upload_bytes = st.upload()
        aux_download = download_bytes / 10000000  # Convert bytes to megabytes
        aux_upload = upload_bytes / 10000000  # Convert bytes to megabytes
        aux_ping = st.results.ping
        # Record measurement times
        tz = pytz.timezone('America/Sao_Paulo')  # Brasília time zone (GMT-3)
        aux_datetime = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        # Store in lists
        download.append(aux_download)
        upload.append(aux_upload)
        ping.append(aux_ping)
        measurement_times.append(aux_datetime)
        
        # Print partial reading
        print(f"Date and time of reading: {aux_datetime} | "
              f"Download Speed: {aux_download:.2f} MB/s | "
              f"Upload Speed: {aux_upload:.2f} MB/s | "
              f"Ping: {aux_ping:.2f} ms", end='\r')
        
        # Check if 9 minutes have passed since the last graph update
        if len(measurement_times) % 3 == 0:  # Update graph every 3 readings (9 minutes)
            print('\nGenerating graph...\n')
            # Create dataframe with network speed data
            data_speeds = {'Download': download, 'Upload': upload, 'Ping': ping}
            data_speeds = pd.DataFrame(data_speeds, columns=['Download', 'Upload', 'Ping'])
            # Create dataframe with measurement times
            df_date_time = pd.DataFrame({'Datetime': measurement_times})
            # Merge the two dataframes
            speed_test_data = pd.concat([df_date_time, data_speeds], axis=1, join='inner')
            # Save the data to a CSV file
            speed_test_data.to_csv("speedtest_data.csv", index=False)
            print('Data saved to speedtest_data.csv\n')
            
            # Generate the graph
            mean_download = np.mean(download)
            mean_upload = np.mean(upload)
            mean_ping = np.mean(ping)
            plt.style.use("ggplot")
            x_pi = len(ping)
            # Array with samples of the number of network speed tests performed
            tests = np.linspace(start=0, stop=x_pi, num=x_pi)
            # Creating the figures
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            # Plotting the graphs
            ax1.plot(tests, download, color='r', label=f'Download Speed. Average: {mean_download:.2f} MB/s')
            ax1.scatter(tests, download, color='r')
            for i, txt in enumerate(download):
                ax1.annotate(f'{txt:.2f}', (tests[i], download[i]), textcoords="offset points", xytext=(0,10), ha='center')
            ax1.set(xlabel="Tests", ylabel="Download Speed in MB/s")
            ax1.legend(loc='best')
            ax2.plot(tests, upload, color='b', label=f'Upload Speed. Average: {mean_upload:.2f} MB/s')
            ax2.scatter(tests, upload, color='b')
            for i, txt in enumerate(upload):
                ax2.annotate(f'{txt:.2f}', (tests[i], upload[i]), textcoords="offset points", xytext=(0,10), ha='center')
            ax2.set(xlabel="Tests", ylabel="Upload Speed in MB/s")
            ax2.legend(loc='best')
            ax3.plot(tests, ping, color='m', label=f'Ping (ms). Average: {mean_ping:.2f} ms')
            ax3.scatter(tests, ping, color='m')
            for i, txt in enumerate(ping):
                ax3.annotate(f'{txt:.2f}', (tests[i], ping[i]), textcoords="offset points", xytext=(0,10), ha='center')
            ax3.set(xlabel="Tests", ylabel="Ping (ms)")
            ax3.legend(loc='best')
            # Show the graphs
            plt.show()
            print('Graph updated.\n')

        print(f'\nThe next test will be performed in 3 minutes...\n')
        time.sleep(180)  # Sleep for 3 minutes
except KeyboardInterrupt:
    print('Program terminated!')
