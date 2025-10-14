import pandas as pd
import matplotlib.pyplot as plt
import json

CSV_FILE = "Datos seguridad.csv"

def load_anomaly_logs(last_n=200):
    df = pd.read_csv(CSV_FILE)

    anomaly_df = df[df['score'] > 0].copy()

    anomaly_df['detected_at'] = pd.to_datetime(anomaly_df['detected_at'])

    def extract_latency(context_str):
        try:
            context = json.loads(context_str)
            return context.get('detect_latency_ms', None)
        except:
            return None

    anomaly_df['detect_latency_ms'] = anomaly_df['context'].apply(extract_latency)

    anomaly_df = anomaly_df.dropna(subset=['detect_latency_ms'])

    anomaly_df = anomaly_df.tail(last_n)

    return anomaly_df

def plot_latency_time_series(df):
    plt.figure(figsize=(14, 6))
    plt.plot(df['detected_at'], df['detect_latency_ms'], marker='o', markersize=2, linewidth=0.5, color='#e74c3c')
    plt.xlabel('Time')
    plt.ylabel('Detection Latency (ms)')
    plt.title('Anomaly Detection Latency Over Time', pad=20)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('latency_time_series.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_latency_histogram(latencies):
    plt.figure(figsize=(10, 6))
    plt.hist(latencies, bins=50, color='#3498db', edgecolor='black', alpha=0.7)
    plt.xlabel('Detection Latency (ms)')
    plt.ylabel('Frequency')
    plt.title('Anomaly Detection Latency Distribution', pad=20)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('latency_histogram.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_latency_by_service(df):
    service_stats = df.groupby('service')['detect_latency_ms'].mean().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))

    services = service_stats.index.tolist()
    avg_latencies = service_stats.values.tolist()

    bars = plt.bar(services, avg_latencies, color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'][:len(services)])
    plt.xlabel('Service')
    plt.ylabel('Average Detection Latency (ms)')
    plt.title('Average Anomaly Detection Latency by Service', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')

    max_latency = max(avg_latencies) if avg_latencies else 0
    plt.ylim(0, max_latency * 1.15)

    for bar, avg in zip(bars, avg_latencies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + (max_latency * 0.02),
                f'{avg:.2f}ms',
                ha='center', va='bottom', fontsize=9, fontweight='bold', rotation=90)

    plt.tight_layout()
    plt.savefig('latency_by_service.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_statistics(latencies):
    print(f"\n{'='*60}")
    print(f"DETECTION LATENCY STATISTICS")
    print(f"{'='*60}")
    print(f"Total anomalies with latency data: {len(latencies)}")
    print(f"Average latency: {latencies.mean():.2f} ms")
    print(f"Min latency: {latencies.min():.2f} ms")
    print(f"Max latency: {latencies.max():.2f} ms")
    print(f"Median latency: {latencies.median():.2f} ms")
    print(f"Std deviation: {latencies.std():.2f} ms")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("Loading anomaly logs...")
    anomaly_df = load_anomaly_logs()

    print(f"Found {len(anomaly_df)} anomalies with latency data")

    latencies = anomaly_df['detect_latency_ms']

    print_statistics(latencies)

    print("Generating charts...")
    plot_latency_time_series(anomaly_df)
    plot_latency_histogram(latencies)
    plot_latency_by_service(anomaly_df)

    print("\nCharts saved:")
    print("  - latency_time_series.png")
    print("  - latency_histogram.png")
    print("  - latency_by_service.png")
