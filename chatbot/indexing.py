from pathlib import Path
from chatbot import config
from chatbot.utils import return_or_throw, extract_attrs

from llama_index.core.indices.base import BaseIndex
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage


DOCUMENTS_FOLDER, INDEXES_PATHS = extract_attrs(config, 'DOCUMENTS_FOLDER', 'INDEXES_PATHS')
FAQ_INDEX_NAME = "faq_index"

def create_faq_index(folder: Path = None, force: bool = False, raise_exception=False) -> None:
    """Creates or overwrites the FAQ index from PDFs."""
    index_path = INDEXES_PATHS / FAQ_INDEX_NAME

    not raise_exception or return_or_throw(index_path.exists() and not force ,
                    FileExistsError(f"Index already exists at {index_path}. Use 'force=True' to overwrite."))

    if index_path.exists() and not force:
        print(f"Index exists at {index_path}. Use 'force=True' to overwrite.")
        return

    documents_folder = return_or_throw(
        folder or config.DOCUMENTS_FOLDER.get('PDF'),
        'PDFs path is not set in the configuration.'
    )
    return_or_throw(documents_folder.exists(), FileNotFoundError(f"Documents folder not found: {documents_folder}"))

    documents = SimpleDirectoryReader(documents_folder).load_data()
    index = VectorStoreIndex.from_documents(documents)
    print(f"Saving index to {index_path}")
    index.storage_context.persist(index_path)


def load_faq_index() -> BaseIndex:
    context = StorageContext.from_defaults(persist_dir=INDEXES_PATHS/FAQ_INDEX_NAME)
    index = load_index_from_storage(context)
    return index

def get_faq_index(force=False) -> BaseIndex:
    create_faq_index(force=force)
    return load_faq_index()

if __name__ == "__main__":
    create_faq_index(force=True)
