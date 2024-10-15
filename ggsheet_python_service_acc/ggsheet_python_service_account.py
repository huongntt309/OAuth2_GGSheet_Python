from googleapiclient.discovery import build
from google.oauth2 import service_account

# Đường dẫn đến tệp JSON chứa thông tin Service Account
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Xác thực với Google bằng Service Account
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Tạo service để kết nối với Google Sheets API
service = build("sheets", "v4", credentials=creds)

# Đọc dữ liệu từ Google Sheet
SAMPLE_SPREADSHEET_ID = "1fZ4eqT47XQnODz0YnHIC6D3mWd1lMDkXsN2FnyqMXlo"
SAMPLE_RANGE_NAME = "Sheet1"

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
values = result.get("values", [])

if not values:
    print("No data found.")
else:
    print("Data retrieved from Google Sheet:")
    for row in values:
        print(row)
