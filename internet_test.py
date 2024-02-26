import time
from datetime import datetime
import speedtest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz

while True:
    try:
        # Inicializar o Speedtest
        st = speedtest.Speedtest()

        # Inicializar as listas/variáveis para armazenar as velocidades medidas
        download = []
        upload = []
        ping = []
        measurement_times = []

        # Interface do programa
        print('------------------------------------------------')
        print('             Internet Speed Test                ')
        print('------------------------------------------------')

        # Execução do teste
        while True:
            # Encontrar o melhor servidor
            print('Finding best server...')
            st.get_best_server()
            print(f'Best server found: {st.results.server["sponsor"]} ({st.results.server["name"]})\n')

            # Calcular as velocidades da internet em megabytes por segundo
            aux_download = st.download()
            aux_upload = st.upload()
            aux_ping = st.results.ping
            # Converter as velocidades para megabits por segundo
            download_mbps = f"{round(aux_download * 1.25e-7, 2)} Mbps"
            upload_mbps = f"{round(aux_upload * 1.25e-7, 2)} Mbps"
            # Registrar os horários das medições
            tz = pytz.timezone('America/Sao_Paulo')  # Fuso horário de Brasília (GMT-3)
            aux_datetime = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            # Armazenar em listas
            download.append(download_mbps)
            upload.append(upload_mbps)
            ping.append(aux_ping)
            measurement_times.append(aux_datetime)
            
            # Imprimir leitura parcial
            print(f"Date and time of reading: {aux_datetime} | "
                f"Download Speed: {download_mbps} | "
                f"Upload Speed: {upload_mbps} | "
                f"Ping: {aux_ping:.2f} ms", end='\r')
            
            # Verificar se passaram 3 minutos desde a última atualização do gráfico
            if len(measurement_times) % 3 == 0:  # Atualizar gráfico a cada 3 leituras (9 minutos)
                print('\nGenerating graph...\n')
                # Criar dataframe com dados de velocidade de rede
                data_speeds = {'Download': download, 'Upload': upload, 'Ping': ping}
                data_speeds = pd.DataFrame(data_speeds, columns=['Download', 'Upload', 'Ping'])
                # Criar dataframe com horários de medição
                df_date_time = pd.DataFrame({'Datetime': measurement_times})
                # Mesclar os dois dataframes
                speed_test_data = pd.concat([df_date_time, data_speeds], axis=1, join='inner')
                # Salvar os dados em um arquivo CSV
                speed_test_data.to_csv("speedtest_data.csv", index=False)
                print('Data saved to speedtest_data.csv\n')
                
                # Gerar o gráfico
                mean_download = np.mean(download)
                mean_upload = np.mean(upload)
                mean_ping = np.mean(ping)
                plt.style.use("ggplot")
                x_pi = len(ping)
                # Array com amostras do número de testes de velocidade de rede realizados
                tests = np.linspace(start=0, stop=x_pi, num=x_pi)
                # Criando as figuras
                fig1, ax1 = plt.subplots(figsize=(10, 5))
                fig2, ax2 = plt.subplots(figsize=(10, 5))
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                # Plotando os gráficos
                ax1.plot(tests, download, color='r', label=f'Download Speed. Average: {mean_download:.2f} Mbps')
                ax1.scatter(tests, download, color='r')
                for i, txt in enumerate(download):
                    ax1.annotate(f'{txt}', (tests[i], download[i]), textcoords="offset points", xytext=(0,10), ha='center')
                ax1.set(xlabel="Tests", ylabel="Download Speed in Mbps")
                ax1.legend(loc='best')
                ax2.plot(tests, upload, color='b', label=f'Upload Speed. Average: {mean_upload:.2f} Mbps')
                ax2.scatter(tests, upload, color='b')
                for i, txt in enumerate(upload):
                    ax2.annotate(f'{txt}', (tests[i], upload[i]), textcoords="offset points", xytext=(0,10), ha='center')
                ax2.set(xlabel="Tests", ylabel="Upload Speed in Mbps")
                ax2.legend(loc='best')
                ax3.plot(tests, ping, color='m', label=f'Ping (ms). Average: {mean_ping:.2f} ms')
                ax3.scatter(tests, ping, color='m')
                for i, txt in enumerate(ping):
                    ax3.annotate(f'{txt:.2f}', (tests[i], ping[i]), textcoords="offset points", xytext=(0,10), ha='center')
                ax3.set(xlabel="Tests", ylabel="Ping (ms)")
                ax3.legend(loc='best')
                # Mostrar os gráficos
                plt.show()
                print('Graph updated.\n')

            print(f'\nThe next test will be performed in 3 minutes...\n')
            time.sleep(180)  # Sleep for 3 minutes
    except KeyboardInterrupt:
        print('Program terminated!')
    except Exception as e:
        print(f'An error occurred: {e}')
        print('Restarting the speed test...\n')
        continue
