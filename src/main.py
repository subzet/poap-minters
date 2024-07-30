import requests
import csv
import os
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GraphQL endpoint
URL = f"https://gateway-arbitrum.network.thegraph.com/api/{os.getenv('THEGRAPH_API_KEY', '')}/subgraphs/id/DWkA5Rpw4z11TXr6DawquZJeXasF4CfyeQy1S2jxCXLH"

# Get event IDs from environment variable
EVENT_IDS = list(map(int, os.getenv('EVENT_IDS', '').split(',')))


def create_query(event_id: int) -> str:
    """Create a GraphQL query for a single event."""
    return f"""
    {{
      events(where: {{ id: "{event_id}" }}) {{
        id
        tokens {{
          id
          mintOrder
          transferCount
          firstTransfer: transfers(
            first: 1,
            orderBy: id,
            orderDirection: asc
          ) {{
            id
            timestamp
            from {{
              id
            }}
            to {{
              id
            }}
          }}
          owner {{
            id
          }}
        }}
      }}
    }}
    """


def fetch_data(event_id: int) -> Dict[str, Any]:
    """Fetch data for a single event from the GraphQL endpoint."""
    query = create_query(event_id)
    response = requests.post(URL, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Query failed for event {event_id} with status code: {response.status_code}")


def process_data(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Process the raw GraphQL data into a list of dictionaries."""
    processed_data = []
    for event in data['data']['events']:
        event_id = event['id']
        for token in event['tokens']:
            processed_data.append({
                'event_id': event_id,
                'token_id': token['id'],
                'mint_order': token['mintOrder'],
                'transfer_count': token['transferCount'],
                'first_transfer_id': token['firstTransfer'][0]['id'] if token['firstTransfer'] else '',
                'first_transfer_timestamp': token['firstTransfer'][0]['timestamp'] if token['firstTransfer'] else '',
                'first_transfer_from': token['firstTransfer'][0]['from']['id'] if token['firstTransfer'] else '',
                'first_transfer_to': token['firstTransfer'][0]['to']['id'] if token['firstTransfer'] else '',
                'current_owner': token['owner']['id']
            })
    return processed_data


def write_to_csv(data: List[Dict[str, str]], filename: str = 'output/poap_minters_data.csv'):
    """Write the processed data to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['event_id', 'token_id', 'mint_order', 'transfer_count',
                      'first_transfer_id', 'first_transfer_timestamp', 'first_transfer_from', 'first_transfer_to', 'current_owner']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


def process_event(event_id: int) -> List[Dict[str, str]]:
    """Process a single event: fetch and process its data."""
    raw_data = fetch_data(event_id)
    return process_data(raw_data)


def main():
    try:
        all_data = []
        with ThreadPoolExecutor() as executor:
            future_to_event = {executor.submit(
                process_event, event_id): event_id for event_id in EVENT_IDS}
            for future in as_completed(future_to_event):
                event_id = future_to_event[future]
                try:
                    data = future.result()
                    all_data.extend(data)
                    print(f"Processed event {event_id}")
                except Exception as exc:
                    print(f"Event {event_id} generated an exception: {exc}")

        write_to_csv(all_data)
        print(f"Data successfully written to poap_minters_data.csv")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
