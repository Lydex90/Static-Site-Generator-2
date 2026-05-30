import os
import shutil
import re
from page_generate import copy_files, extract_title, generate_page, generate_pages_recursive
import sys

def main():
    docs_path = os.path.join(os.path.dirname(__file__), "../docs")
    static_path = os.path.join(os.path.dirname(__file__), "../static")
    if len(sys.argv) > 1 and sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    shutil.rmtree(docs_path)
    os.makedirs(docs_path)
    copy_files(static_path, docs_path)
    generate_pages_recursive("content","template.html",docs_path, basepath)


main()