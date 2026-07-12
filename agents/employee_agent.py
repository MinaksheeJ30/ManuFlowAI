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

sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Employees")


def employee_agent(machine):

    rows = sheet.get_all_records()

    # Employees belonging to the required department
    candidates = [
        row for row in rows
        if row["Department"].strip().lower() == machine.strip().lower()
    ]

    if not candidates:
        return None

    # Employee with minimum workload
    employee = min(
        candidates,
        key=lambda x: int(x["Current Tasks"])
    )

    # Update workload
    cell = sheet.find(employee["Employee ID"])

    task_column = 5      # Current Tasks column

    current = int(employee["Current Tasks"])

    sheet.update_cell(cell.row, task_column, current + 1)

    return employee