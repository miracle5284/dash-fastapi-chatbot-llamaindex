from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BaseFolder = Path(__file__).parent

PDFs = 'documents/PDFs'


DOCUMENTS_FOLDER = {
    "PDF": BaseFolder / PDFs
}

INDEXES_PATHS = "store"





###############################
INDEXES_PATHS = BaseFolder / INDEXES_PATHS