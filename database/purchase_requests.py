import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from app.config import GOOGLE_SHEET_NAME

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials/service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Purchase_Requests")


def add_purchase_request(request):

    purchase_id = "PR-" + datetime.now().strftime("%Y%m%d%H%M%S")

    sheet.append_row([
        purchase_id,
        request["material"],
        request["qty_to_order"],
        "Not Assigned",
        request["status"],
        datetime.now().strftime("%d-%b-%Y")
    ])

    print(f"Purchase Request {purchase_id} created.")