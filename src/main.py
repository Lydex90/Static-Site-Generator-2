from textnode import TextType, TextNode
import os
import shutil
import re
from markdwn_to_text import markdown_to_html_node


def main():
    public_path = os.path.join(os.path.dirname(__file__), "../public")
    static_path = os.path.join(os.path.dirname(__file__), "../static")
    shutil.rmtree(public_path)
    os.makedirs(public_path)
    copy_files(static_path, public_path)
    generate_page("content/index.md","template.html","public/index.html")

def copy_files(src, dst):
    for item in os.scandir(src):
        if item.is_dir():
            new_dst = os.path.join(dst, item.name)
            os.makedirs(new_dst, exist_ok=True)
            copy_files(item.path, new_dst)
        else:
            shutil.copy(item.path, dst)

def extract_title(markdown):
    h1 = re.search(r'^# (.+)$', markdown, re.MULTILINE)
    if not h1:
        raise Exception("No header found")
    return h1.group(1)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    with open(from_path, 'r') as f:
        from_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    from_converted = markdown_to_html_node(from_content)
    from_converted = from_converted.to_html()
    title = extract_title(from_content)
    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", from_converted)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(result)
     


main()