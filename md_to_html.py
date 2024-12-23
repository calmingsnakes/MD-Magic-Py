import re

def convert_markdown_to_html(md_content):
    """
    Convert a subset of Markdown (headers) to HTML.
    """
    lines = md_content.splitlines()
    html_lines = []
    
    for line in lines:
        # Convert Markdown headers (e.g., ## Header) to HTML headers (e.g., <h2>Header</h2>)
        header_match = re.match(r'^(#+)\s*(.*)', line)
        if header_match:
            level = len(header_match.group(1))  # Number of '#' determines header level
            title = header_match.group(2)
            html_lines.append(f'<h{level}>{title}</h{level}>')
        else:
            # Simple paragraph handling (you can expand this for other Markdown features)
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)

def generate_toc_and_add_ids(html_content):
    """
    Generate a Table of Contents (TOC) and add IDs to HTML headers.
    """
    toc = []
    headers = re.findall(r'<h([1-6])>(.*?)</h[1-6]>', html_content)

    # Replace headers with IDs and generate TOC
    for i, (level, title) in enumerate(headers):
        header_id = title.replace(' ', '-').lower()  # Generate an ID by replacing spaces with dashes
        toc.append({
            'level': int(level),
            'title': title,
            'id': header_id
        })
        # Replace original header with header that has an id
        html_content = html_content.replace(
            f'<h{level}>{title}</h{level}>',
            f'<h{level} id="{header_id}">{title}</h{level}>'
        )

    # Build the TOC HTML
    toc_html = "<nav id='toc'><ul>\n"
    for item in toc:
        toc_html += f"<li style='margin-left:{(item['level'] - 1) * 20}px'><a href='#{item['id']}'>{item['title']}</a></li>\n"
    toc_html += "</ul></nav>\n"

    return toc_html + html_content

def inject_css(html_content):
    """
    Inject basic CSS styling into the HTML content.
    """
    css = """
    <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: row;
    }
    #toc {
        width: 20%;
        background-color: #f4f4f4;
        padding: 20px;
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        overflow-y: auto;
        box-sizing: border-box;
    }
    #content {
        margin-left: 20%;
        padding: 20px;
        width: 80%;
        box-sizing: border-box;
    }
    nav ul {
        list-style-type: none;
        padding-left: 0;
    }
    nav ul li {
        margin-bottom: 10px;
    }
    nav ul li a {
        text-decoration: none;
        color: #007BFF;
    }
    nav ul li a:hover {
        text-decoration: underline;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }
    p {
        line-height: 1.6;
    }
    </style>
    """
    return css + html_content

def markdown_to_html_with_toc(md_file_path, output_html_path):
    """
    Read the Markdown file, convert it to HTML, generate TOC, and write the output HTML file.
    """
    # Read the markdown file
    with open(md_file_path, 'r') as md_file:
        md_content = md_file.read()

    # Convert markdown to HTML
    html_content = convert_markdown_to_html(md_content)

    # Generate the Table of Contents and add IDs to headers
    full_html = generate_toc_and_add_ids(html_content)

    # Wrap content in a div for styling
    full_html = f"<div id='content'>\n{full_html}\n</div>"

    # Inject CSS for basic styling and layout
    full_html = inject_css(full_html)

    # Write the final HTML to an output file
    with open(output_html_path, 'w') as html_file:
        html_file.write(full_html)

# Example usage
markdown_to_html_with_toc('input.md', 'output.html')
