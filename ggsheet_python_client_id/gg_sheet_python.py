import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes cho phép quyền truy cập Google Sheets và Google Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.readonly']

# Tên file credentials bạn tải xuống từ Google Cloud
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def authenticate_google():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def get_sheet_data(spreadsheet_id, range_name):
    creds = authenticate_google()
    
    # Tạo service để gọi Google Sheets API
    service = build('sheets', 'v4', credentials=creds)
    
    # Gọi Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return []

    return values

# Thay thế bằng Spreadsheet ID và phạm vi (range) mà bạn muốn truy xuất dữ liệu
SPREADSHEET_ID = '1fZ4eqT47X________________XsN2FnyqMXlo'
RANGE_NAME = 'Sheet1!A1:D10'

# Gọi hàm để lấy dữ liệu từ Google Sheet
data = get_sheet_data(SPREADSHEET_ID, RANGE_NAME)
print(data)
