import os
import subprocess

# Define the directories relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, '..'))
input_dir = os.path.join(repo_root, 'mermaid')
output_dir = os.path.join(repo_root, 'mermaid_images')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over all .md files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.md'):
        input_filepath = os.path.join(input_dir, filename)
        output_filepath = os.path.join(output_dir, filename.replace('.md', '.png'))
        
        # Generate the image using mermaid-cli directly from the .md file
        subprocess.run(['mmdc', '-i', input_filepath, '-o', output_filepath])

print("Mermaid diagrams have been converted to images in the 'mermaid_images' folder.")