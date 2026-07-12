import gspread
from google.oauth2.service_account import Credentials

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

sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Inventory")


def check_inventory(material, required_qty):

    rows = sheet.get_all_records()

    for row in rows:

        if row["Material"].lower() == material.lower():

            stock = int(row["Available_Qty"])

            return {
                "available": stock >= required_qty,
                "stock": stock,
                "required": required_qty
            }

    return {
        "available": False,
        "stock": 0,
        "required": required_qty
    }