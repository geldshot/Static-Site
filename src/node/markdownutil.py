import re

from .htmlutil import markdown_to_html_node


def extract_title(markdown):
    regex = "(?:^|\\n)# (.*)"
    title = re.findall(regex, markdown)

    if not title or not title[0]:
        raise Exception("no title header")
    
    return title[0]

# this would be a perfect place for a t string if that wasn't so painfully new that I don't have it yet

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path).read()
    template_file = open(template_path).read()
    
    content = markdown_to_html_node(md_file).to_html()

    title = extract_title(md_file)

    output = template_file.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    with open (dest_path, "w") as file:
        file.write(output)