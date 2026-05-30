from markdwn_to_text import markdown_to_html_node
from textnode import TextType, TextNode
import os
import shutil
import re


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

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    with open(from_path, 'r') as f:
        from_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    from_converted = markdown_to_html_node(from_content)
    from_converted = from_converted.to_html()
    title = extract_title(from_content)
    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", from_converted).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    get_all_files = os.listdir(dir_path_content)
    print(f"generating page recursive on these files {get_all_files}")
    for file in get_all_files:
        full_path = os.path.join(dir_path_content, file)
        print(f"checking file {file}")
        if full_path.endswith('.md'):
            dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
            generate_page(full_path,template_path,dest_path, base_path)
        elif os.path.isdir(full_path):
            new_dest = os.path.join(dest_dir_path, file)
            generate_pages_recursive(full_path, template_path, new_dest, base_path)
        