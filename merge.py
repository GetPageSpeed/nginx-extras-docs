import os

def create_master_md(source_dir, output_file):
    """
    Concatenates all markdown files in the source directory into a single master markdown file.

    Args:
    source_dir (str): The directory containing the markdown files.
    output_file (str): The path of the master markdown file to create.
    """
    with open(output_file, 'w') as master_file:
        for root, dirs, files in os.walk(source_dir):
            for file in sorted(files):
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        master_file.write(f.read() + '\n\n')

# Usage
create_master_md('docs/modules', 'master_document_nginx_modules.md')
