import sched
import time
import json
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Inicializa o agendador
task_scheduler = sched.scheduler()

# Listas para armazenar os dados coletados
datetime = []
download = []
upload = []
ping = []
jitter = []
packet_loss = []
low_latency = []
high_latency = []
result_urls = []

# Nome do arquivo CSV
CSV_FILE = "speedtest_results.csv"

# Interface
print('------------------------------------------------')
print('       Teste - Velocidade Internet Ookla        ')
print('------------------------------------------------')
print('Para interromper o programa, pressione Crtl+C.')


def delay():
    while True:
        delay_time = input('Digite o intervalo em segundos entre cada teste de velocidade de internet: ')
        if delay_time.isnumeric():
            return int(delay_time)
        print('Digite apenas números!')

delay_time = delay()


def run_speedtest():
    print('\nExecutando Speedtest...')
    try:
        result = subprocess.run(
            [r"c:\\Users\\Carlos\\Downloads\\ookla-speedtest-1.2.0-win64\\speedtest.exe", "--format=json"],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        # Verifique se a chave "result" e "url" existem
        aux_result_url = data.get("result", {}).get("url", "N/A")  # Usa "N/A" se não existir
        
        # Atualize as demais variáveis com verificações similares
        aux_packet_loss = data.get("packetLoss", 0)  # Exemplo para packetLoss
        
        aux_datetime = time.ctime()
        aux_download = data["download"]["bandwidth"] / 125000
        aux_upload = data["upload"]["bandwidth"] / 125000
        aux_ping = data["ping"]["latency"]
        aux_jitter = data["ping"]["jitter"]
        aux_low_latency = data["ping"].get("low", 0)
        aux_high_latency = data["ping"].get("high", 0)
        # aux_packet_loss = data.get("packetLoss", 0)
        # aux_result_url = data["result"]["url"]
        
        datetime.append(aux_datetime)
        download.append(aux_download)
        upload.append(aux_upload)
        ping.append(aux_ping)
        jitter.append(aux_jitter)
        low_latency.append(aux_low_latency)
        high_latency.append(aux_high_latency)
        packet_loss.append(aux_packet_loss)
        result_urls.append(aux_result_url)

        print(f"Latência: {aux_ping:.2f} ms (Jitter: {aux_jitter:.2f} ms)")
        print(f"Download: {aux_download:.2f} Mbps")
        print(f"Upload: {aux_upload:.2f} Mbps")
        print(f"Baixa Latência: {aux_low_latency:.2f} ms | Alta Latência: {aux_high_latency:.2f} ms")
        print(f"Perda de Pacotes: {aux_packet_loss}%")
        print(f"Resultado Online: {aux_result_url}\n")

        save_results()
    
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print("Erro ao executar o Speedtest:", e)

    task_scheduler.enter(delay=delay_time, priority=0, action=run_speedtest)


def save_results():
    new_data = pd.DataFrame({
        "Datetime": datetime,
        "Download (Mbps)": download,
        "Upload (Mbps)": upload,
        "Ping (ms)": ping,
        "Jitter (ms)": jitter,
        "Low Latency (ms)": low_latency,
        "High Latency (ms)": high_latency,
        "Packet Loss (%)": packet_loss,
        "Result URL": result_urls
    })
    
    if os.path.exists(CSV_FILE):
        new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        new_data.to_csv(CSV_FILE, mode='w', header=True, index=False)
    
    print("Resultados salvos em speedtest_results.csv")


def plot_results():
    plt.style.use("ggplot")
    x = range(len(datetime))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, download, label='Download (Mbps)', color='r')
    ax.plot(x, upload, label='Upload (Mbps)', color='b')
    ax.plot(x, ping, label='Ping (ms)', color='g')
    ax.plot(x, jitter, label='Jitter (ms)', color='purple')
    ax.set_xlabel("Testes")
    ax.set_ylabel("Valores")
    ax.legend()
    plt.title("Evolução da Conexão de Internet")
    plt.savefig("internet_speed_graph.png")
    
    try:
        plt.show()  # Exibe o gráfico
    except KeyboardInterrupt:
        plt.close()  # Fecha a janela do gráfico se houver interrupção
        print("\nGráfico fechado pelo usuário.")
    
    print("Gráfico salvo como internet_speed_graph.png")


try:
    run_speedtest()
    task_scheduler.run(blocking=True)
except KeyboardInterrupt:
    save_results()
    plot_results()
    print("Programa finalizado!")
