import pandas as pd
from googleapiclient.discovery import build

# YouTube Data API credentials
API_KEY = ''

# Create the YouTube service
youtube = build('youtube', 'v3', developerKey=API_KEY)

def check_channel_exists(channel_name):
    try:
        # Search for the channel by name
        request = youtube.search().list(
            q=channel_name,
            type='channel',
            part='snippet',
            maxResults=1
        )
        response = request.execute()

        # Check if any items were returned
        if response['items']:
            channel_title = response['items'][0]['snippet']['title'].lower()
            # Compare the channel title with the queried channel name
            if channel_name.lower() == channel_title:
                return "Available"
            else:
                return "Not Available"
        else:
            return "Not Found2"
    except Exception as e:
        return f"Error: {str(e)}"

def process_excel(file_path, sheet_name):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Check if the necessary columns exist
    if 'YouTube Channel' not in df.columns:
        print("Error: 'YouTube Channel' column not found in Excel sheet.")
        return
    
    # Create a new column for the status
    df['Channel Status'] = df['YouTube Channel'].apply(check_channel_exists)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, sheet_name=sheet_name, index=False)
    print(f"Updated Excel file saved: {file_path}")

# Usage example
file_path = '\checkytlist.xlsx' #Replace with actual file path
sheet_name = 'Sheet1'  # Replace with your actual sheet name
process_excel(file_path, sheet_name)
