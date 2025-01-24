import os
from xml.etree import ElementTree as ET
from datetime import datetime

# Base directory containing SVG files (with subfolders)
SVG_DIR = "icons"  # Base icons folder relative to the script
PLUGIN_NAMESPACE = "estd/kirby-remix-icons"  # Namespace for the Kirby plugin

def extract_svg_content(svg_file):
    """
    Extracts the SVG content from a file and removes specific attributes.
    """
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
        # Remove namespaces for simplicity
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        # Remove viewBox attribute if it matches "0 0 24 24"
        if root.attrib.get('viewBox') == "0 0 24 24":
            del root.attrib['viewBox']
        # Convert back to string
        svg_content = ET.tostring(root, encoding='unicode', method='xml')
        return svg_content
    except Exception as e:
        print(f"Error processing {svg_file}: {e}")
        return None


def escape_for_php(string):
    """
    Escapes single quotes for PHP.
    """
    return string.replace("'", "\\'")

def generate_kirby_plugin(svg_dir, namespace):
    """
    Generates Kirby plugin index.php and index.js files.
    """
    start_time = datetime.now()
    
    if not os.path.isdir(svg_dir):
        print(f"SVG directory '{svg_dir}' not found!")
        return
    
    # Statistics tracking
    total_files = 0
    successful_icons = 0
    failed_icons = 0
    categories = set()
    
    # Collect icon data
    icons_php = []
    icons_js = []
    for root_dir, _, files in os.walk(svg_dir):
        category = os.path.basename(root_dir)
        if category != "icons":  # Skip the base directory name
            categories.add(category)
            
        for file_name in files:
            if file_name.endswith(".svg"):
                total_files += 1
                icon_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(root_dir, file_name)
                svg_content = extract_svg_content(file_path)
                if svg_content:
                    successful_icons += 1
                    # Escape single quotes for PHP
                    escaped_svg_content = escape_for_php(svg_content)
                    # Add to PHP array
                    icons_php.append("'{}' => '{}'".format(icon_name, escaped_svg_content))
                    # Add to JS object
                    icons_js.append("'{}': `{}`".format(icon_name, svg_content))
                else:
                    failed_icons += 1
    
    # Write index.php using regular string formatting
    php_template = """<?php

Kirby::plugin('{}', [
    'icons' => [
        {}
    ]
]);
"""
    php_content = php_template.format(
        namespace,
        ',\n        '.join(icons_php)
    )
    
    with open("index.php", "w", encoding="utf-8") as php_file:
        php_file.write(php_content)
    
    # Write index.js using regular string formatting
    js_template = """panel.plugin('{}', {{
    icons: {{
        {}
    }}
}});
"""
    js_content = js_template.format(
        namespace,
        ',\n        '.join(icons_js)
    )
    
    with open("index.js", "w", encoding="utf-8") as js_file:
        js_file.write(js_content)
    
    # Calculate execution time
    execution_time = (datetime.now() - start_time).total_seconds()
    
    # Print summary
    print("\n=== Icon Generation Summary ===")
    print(f"Time taken: {execution_time:.2f} seconds")
    print(f"Total SVG files found: {total_files}")
    print(f"Successfully processed: {successful_icons}")
    print(f"Failed to process: {failed_icons}")
    print(f"Categories found: {len(categories)}")
    print("Categories:")
    for category in sorted(categories):
        category_count = len([f for f in os.listdir(os.path.join(svg_dir, category)) 
                            if f.endswith('.svg')])
        print(f"  - {category}: {category_count} icons")
    print(f"\nGenerated files:")
    print(f"  - index.php: {os.path.getsize('index.php'):,} bytes")
    print(f"  - index.js: {os.path.getsize('index.js'):,} bytes")

# Run the generator
generate_kirby_plugin(SVG_DIR, PLUGIN_NAMESPACE)