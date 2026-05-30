import os
import shutil
import re
from page_generate import copy_files, extract_title, generate_page, generate_pages_recursive


def main():
    public_path = os.path.join(os.path.dirname(__file__), "../public")
    static_path = os.path.join(os.path.dirname(__file__), "../static")
    shutil.rmtree(public_path)
    os.makedirs(public_path)
    copy_files(static_path, public_path)
    generate_pages_recursive("content","template.html","public")


main()