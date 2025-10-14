import requests
import json
from typing import Dict, List, Any
import time
import matplotlib.pyplot as plt

ENDPOINT_URL = "http://localhost:9000/invoice/calculate"

def send_request(items: List[Dict[str, int]], endpoint: str = ENDPOINT_URL) -> Dict[str, Any]:
    payload = {"items": items}

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def create_pie_chart(response_data: Dict[str, Any], reference_value: float):
    labels = []
    values = []
    colors = []

    final_total = response_data.get('finalTotal', 0)
    labels.append('Coordinator')
    values.append(final_total)
    colors.append('#2ecc71' if final_total == reference_value else '#e74c3c')

    for vote in response_data.get('votes', []):
        service = vote.get('service', 'Unknown')
        total = vote.get('total', 0)
        labels.append(service.capitalize())
        values.append(total)
        colors.append('#3498db' if total == reference_value else '#e67e22')

    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=labels, autopct='%1.2f%%', colors=colors, startangle=90)
    plt.title(f'Total Comparison vs Reference Value: ${reference_value}', pad=20)

    legend_labels = [
        f'{label}: ${value:.2f}' for label, value in zip(labels, values)
    ]
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.savefig('comparison_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

    print(f"\nChart saved as 'comparison_chart.png'")


def test_multiple_requests_one_minute():
    items = [
        {"productId": 1, "quantity": 10},
        {"productId": 2, "quantity": 15}
    ]

    num_requests = int(input("Number of requests to send: "))
    reference_value = float(input("Expected reference value: "))

    results = []
    start_time = time.time()

    for i in range(num_requests):
        print(f"Sending request {i+1}/{num_requests}...")
        result = send_request(items)
        if result:
            results.append(result)
        time.sleep(60 / num_requests)

    elapsed_time = time.time() - start_time

    coordinator_matches = 0
    python_matches = 0
    java_matches = 0
    csharp_matches = 0
    total_responses = len(results)

    for result in results:
        if result.get('finalTotal') == reference_value:
            coordinator_matches += 1

        for vote in result.get('votes', []):
            service = vote.get('service', '').lower()
            total = vote.get('total', 0)

            if total == reference_value:
                if service == 'python':
                    python_matches += 1
                elif service == 'java':
                    java_matches += 1
                elif service == 'csharp':
                    csharp_matches += 1

    print(f"\n{'='*60}")
    print(f"ANALYSIS RESULTS")
    print(f"{'='*60}")
    print(f"Total requests: {num_requests}")
    print(f"Successful responses: {total_responses}")
    print(f"Reference value: ${reference_value}")
    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"\n{'='*60}")
    print(f"Matches the expected total invoice value")
    print(f"{'='*60}")

    if total_responses > 0:
        coord_pct = (coordinator_matches / total_responses) * 100
        python_pct = (python_matches / total_responses) * 100
        java_pct = (java_matches / total_responses) * 100
        csharp_pct = (csharp_matches / total_responses) * 100

        print(f"Coordinator: {coordinator_matches}/{total_responses} ({coord_pct:.2f}%)")
        print(f"Python: {python_matches}/{total_responses} ({python_pct:.2f}%)")
        print(f"Java: {java_matches}/{total_responses} ({java_pct:.2f}%)")
        print(f"C#: {csharp_matches}/{total_responses} ({csharp_pct:.2f}%)")

        labels = ['Coordinator', 'Python', 'Java', 'C#']
        percentages = [coord_pct, python_pct, java_pct, csharp_pct]
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']

        plt.figure(figsize=(10, 8))
        bars = plt.bar(labels, percentages, color=colors)
        plt.ylabel('Match Percentage (%)')
        plt.title(f'Matches the expected total invoice value: ${reference_value}', pad=20)
        plt.ylim(0, 110)

        for bar, pct in zip(bars, percentages):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{pct:.1f}%',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.savefig('accuracy_chart.png', dpi=300, bbox_inches='tight')
        plt.show()

        print(f"\nChart saved as 'accuracy_chart.png'")


if __name__ == "__main__":
    test_multiple_requests_one_minute()
