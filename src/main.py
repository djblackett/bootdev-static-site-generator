
import sys
from markdown_to_html_node import markdown_to_html_node
from textnode import TextNode, TextType
import os
import shutil
from pathlib import Path


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    try:
        # Ensure the public directory is cleaned up before starting
        cleanup()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Copy static files to public directory
    public_path = os.path.join(Path.cwd(), "docs")
    static_path = os.path.join(Path.cwd(), "static")

    copy_static_files(static_path, public_path)

    src_path = os.path.join(Path.cwd(), "content")
    dst_path = os.path.join(Path.cwd(), "docs")
    template_path = os.path.join(Path.cwd(), "template.html")
    generate_pages_recursive(src_path, template_path, dst_path, basepath)
    print("Static site generator completed successfully.")


def copy_static_files(src, dst):

    filelist = os.listdir(src)
    # print(filelist)

    if not os.path.exists(dst):
        os.makedirs(dst)

    # Copy each file from src to dst
    # print(f"Copying files from {src} to {dst}")
    for file in filelist:
        filepath = os.path.join(src, file)
        if os.path.isfile(filepath):
            # print(f"Copying {file} to {dst}")
            shutil.copyfile(filepath, os.path.join(dst, file))
        else:
            copy_static_files(os.path.join(src, file), os.path.join(dst, file))


def cleanup():
    public_path = os.path.join(Path.cwd(), "public")
    static_path = os.path.join(Path.cwd(), "static")

    # print(public_path)

    if not os.path.exists(static_path):
        raise FileNotFoundError(
            f"Static directory does not exist: {static_path}")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)


def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception(
            "Markdown must start with a title in the format '# Title'")
    title = markdown.split("\n")[0][2:].strip()
    return title


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} using template {template_path} to {dest_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

        title = extract_title(markdown)
        html = markdown_to_html_node(markdown).to_html()

        with open(template_path, "r") as f:
            template = f.read()

            # Replace the title and content in the template
            html = template.replace("{{ Title }}", title).replace(
                "{{ Content }}", html)
            html = html.replace("href=\"/", f"href=\"{basepath}")
            html = html.replace("src=\"/", f"src=\"{basepath}")

            Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "w") as f:
                f.write(html)
    print(f"Page generated at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    filelist = os.listdir(dir_path_content)
    # print(filelist)

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for file in filelist:
        filepath = os.path.join(dir_path_content, file)

        if os.path.isdir(filepath):
            # If it's a directory, recurse into it
            dst = os.path.join(dest_dir_path, file)
            generate_pages_recursive(filepath, template_path, dst, basepath)
        elif file.endswith(".md"):
            # If it's a markdown file, generate a page for it
            dst_path = os.path.join(
                dest_dir_path, file.replace(".md", ".html"))
            generate_page(filepath, template_path, dst_path, basepath)


main()
