import os
import pymupdf
import pandas as pd
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from datetime import timedelta, datetime, date

def is_due(state):
    if not state.exists():
        return True
    last = date.fromisoformat(state.read_text().strip())
    print(f"Email notification was last sent on: {last}")
    return date.today() - last >= timedelta(days=15)

def get_pdf_text(filename):
    with pymupdf.open(filename) as doc: 
        pages = []
        for page in doc:
            text = page.get_text("text") 
            pages.append(text.strip()) 
        output = "\n".join(pages)
        #fallback to ocr
        if len(output.strip()) < 20:
            try:
                pix = doc[0].get_pixmap(dpi=200, colorspace=pymupdf.csRGB, alpha=False)
                arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                result, elapse = RapidOCR()(arr)
                text = "\n".join(line[1] for line in result)
                return text
            except:
                return ""
        return output
    
def get_expired(expiry_date, days_ahead):
    date_format = "%d-%b-%Y" 
    current_date = date.today()
    
    ##Handle NA cases
    if any(x in expiry_date for x in ("NA", "N/A")):
        expiry_date_dt = current_date - timedelta(days=1)

    ##Handle normal cases
    else:
        expiry_date_dt = datetime.strptime(expiry_date, date_format).date()
    
    date_diff = expiry_date_dt - current_date
    
    if 0 < date_diff.days < days_ahead:
        return date_diff.days
    else:
        return False

def get_all_filepaths(folder: str) -> list[str]:
    full_paths = []
    
    for dirpath, _, filenames in os.walk(folder):
        for name in filenames:
            full_paths.append(os.path.join(dirpath, name))
    return full_paths

def parsed_files(gcp_filepath=[], div_filepath=[], tdg_filepath=[]):
    file_data = {}
    
    for f in [*gcp_filepath, *div_filepath, *tdg_filepath]:
        if f.lower().endswith(".pdf"):
            filename = os.path.basename(f)
            file_data[filename] = {'certificate_text': get_pdf_text(f)}

    return file_data

def get_filenames(all_files):
    filenames = list(examples.keys())
    return filenames

def load_certificates(path, dayfirst=False):
    """Read the CSV and convert expiry_date to datetimes (bad values become NaT)."""
    df = pd.read_csv(path)
    df["expiry_date"] = pd.to_datetime(df["expiry_date"], errors="coerce", dayfirst=dayfirst)
    return df

def format_record(name, course, expiry, date_format="%d %b %Y"):
    """Build the 3-line paragraph for one person."""
    expiry_text = "Not provided" if pd.isna(expiry) else expiry.strftime(date_format)
    return (
        f"Name: {name}\n"
        f"Course: {course}\n"
        f"Expiry Date: {expiry_text}"
    )

def format_certificates(df, date_format="%d %b %Y", dayfirst=False):
    """Take a DataFrame with name, course, expiry_date and return all paragraphs as one string."""
    expiry = pd.to_datetime(df["expiry_date"], errors="coerce", dayfirst=dayfirst)
    paragraphs = [
        format_record(name, course, exp, date_format)
        for name, course, exp in zip(df["cert_owner"], df["course_name"], expiry)
    ]
    return "\n\n".join(paragraphs)