import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from app.config import GOOGLE_SHEET_NAME, GOOGLE_WORKSHEET_NAME
from app.utils import generate_job_id

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials/service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)


def add_job(job):

    spreadsheet = client.open(GOOGLE_SHEET_NAME)
    sheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)

    if job.job_id is None:
        job.job_id = generate_job_id(sheet)

    if job.date_created is None:
        job.date_created = datetime.now().strftime("%d-%b-%Y")

    row = [
        job.job_id,
        job.date_created,
        job.part_name,
        job.material,
        job.quantity,
        job.machine,
        job.deadline,
        job.assigned_to,
        job.status,
        job.estimated_time,
        job.remarks
    ]

    result = sheet.append_row(row)

    print(result)