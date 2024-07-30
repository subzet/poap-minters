# POAP Minters Data Fetcher

This script fetches POAP (Proof of Attendance Protocol) minter data for specific events using GraphQL queries and outputs the results to a CSV file. It processes multiple events in parallel for improved efficiency.

## Requirements

- Python 3.7+
- Required Python packages are listed in `requirements.txt`

## Setup

1. Clone this repository or download the script files.

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the same directory as the script with the following content:

   ```
   EVENT_IDS=2796,432,257,259,258,260
   THEGRAPH_API_KEY=YOUR_API_KEY
   ```

   Replace the numbers with the event IDs you want to fetch data for.

## Usage

Run the script using Python:

```
python poap_minters_fetcher.py
```

The script will fetch data for all specified event IDs in parallel and create a CSV file named `poap_minters_data.csv` in the same directory.

## Output

The generated CSV file will contain the following columns for each token:

- event_id
- token_id
- mint_order
- transfer_count
- first_transfer_id
- first_transfer_from
- first_transfer_to
- current_owner

## Customization

- To change the output file name, modify the `filename` parameter in the `write_to_csv` function call within the `main` function.
- To modify the GraphQL endpoint, update the `URL` variable at the top of the script.

## Error Handling

The script includes basic error handling:

- If fetching data for a specific event fails, it will print an error message and continue with the next event.
- If any other error occurs during execution, it will print a general error message.

## Contributing

Feel free to fork this repository and submit pull requests with any enhancements.

## License

This project is open source and available under the [MIT License](LICENSE).