import os
import yaml

def update_yaml_in_md_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Check if the file has YAML front matter
                if lines[0].strip() == '---':
                    # Find the end of the YAML front matter
                    yaml_end_index = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == '---'), None)
                    if yaml_end_index is not None:
                        yaml_content = ''.join(lines[1:yaml_end_index])
                        content = ''.join(lines[yaml_end_index + 1:])
                        
                        # Parse and update YAML
                        yaml_data = yaml.safe_load(yaml_content)
                        if 'date' in yaml_data:
                            yaml_data['pubDate'] = yaml_data.pop('date')      
                        if 'description' not in yaml_data:
                            # 取出文章前 100 个字符作为文章描述
                            yaml_data['description'] = content[:100]            
                        
                        updated_yaml = yaml.dump(yaml_data, sort_keys=False)
                        
                        # Write updated content back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('---\n')
                            f.write(updated_yaml)
                            f.write('---\n')
                            f.write(content)

if __name__ == "__main__":
    content_dir = os.path.join(os.path.dirname(__file__), "../content")
    update_yaml_in_md_files(content_dir)