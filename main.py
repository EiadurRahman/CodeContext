import os
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

def get_project_structure(directory):
    """Generate a tree-like structure of the project."""
    tree = []
    for root, dirs, files in os.walk(directory):
        # Skip .git directories
        dirs[:] = [d for d in dirs if d != '.git']
        
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            # Skip git-related files
            if not is_git_file(file):
                tree.append(f"{sub_indent}{file}")
    return '\n'.join(tree)

def is_git_file(file_name):
    """Check if a file is git-related."""
    git_files = ['.gitignore', '.gitattributes', '.gitmodules', '.gitkeep']
    return file_name in git_files or file_name.startswith('.git')

def is_binary_file(file_path):
    """Check if a file is binary or text."""
    try:
        with open(file_path, 'tr') as f:
            f.read(1024)
        return False
    except UnicodeDecodeError:
        return True

def should_include_file(file_path):
    """Determine if a file should be included in the context document."""
    # Check if it's in a .git directory
    if '/.git/' in file_path or file_path.endswith('/.git'):
        return False
    
    # Check if it's a git file
    if is_git_file(os.path.basename(file_path)):
        return False
        
    # Avoid media and binary files
    if is_binary_file(file_path):
        return False
        
    # List of file extensions to exclude
    excluded_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',  # Images
        '.mp3', '.wav', '.ogg', '.flac',  # Audio
        '.mp4', '.avi', '.mov', '.mkv',  # Video
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Documents
        '.zip', '.tar', '.gz', '.rar',  # Archives
        '.pyc', '.pyo', '.pyd',  # Python compiled files
        '.so', '.dll', '.exe',  # Binaries
        '.db', '.sqlite', '.sqlite3',  # Databases
    ]
    
    _, ext = os.path.splitext(file_path)
    return ext.lower() not in excluded_extensions

def extract_code_from_project(directory):
    """Extract code from the project directory."""
    code_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip .git directories
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        relative_path = os.path.relpath(file_path, directory)
                        code_files.append((relative_path, content))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return code_files

def generate_pdf(project_name, directory, output_file):
    """Generate a PDF containing project context."""
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12
    )
    
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10
    )
    
    code_path_style = ParagraphStyle(
        'CodePath',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=12,
        textColor=colors.blue,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=10,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=20,
        backColor=colors.lightgrey
    )
    
    # Create the document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    story = []
    
    # Add title
    story.append(Paragraph(f"Project Context: {project_name}", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add project structure
    story.append(Paragraph("Project Structure", heading_style))
    structure = get_project_structure(directory)
    story.append(Preformatted(structure, styles["Code"]))
    story.append(Spacer(1, 0.3*inch))
    
    # Add code files
    story.append(Paragraph("Project Files", heading_style))
    
    code_files = extract_code_from_project(directory)
    for file_path, content in code_files:
        story.append(Paragraph(file_path, code_path_style))
        
        # Format code with syntax highlighting (basic)
        formatted_code = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        code_block = Preformatted(formatted_code, styles["Code"])
        story.append(code_block)
        story.append(Spacer(1, 0.2*inch))
    
    # Build the PDF
    doc.build(story)

def generate_markdown(project_name, directory, output_file):
    """Generate a Markdown document containing project context."""
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # Add title
        md_file.write(f"# Project Context: {project_name}\n\n")
        
        # Add project structure
        md_file.write("## Project Structure\n\n")
        md_file.write("```\n")
        structure = get_project_structure(directory)
        md_file.write(structure)
        md_file.write("\n```\n\n")
        
        # Add code files
        md_file.write("## Project Files\n\n")
        
        code_files = extract_code_from_project(directory)
        for file_path, content in code_files:
            md_file.write(f"### {file_path}\n\n")
            
            # Determine language for syntax highlighting
            file_extension = os.path.splitext(file_path)[1][1:]
            language = get_language_from_extension(file_extension)
            
            # Add code block with syntax highlighting
            md_file.write(f"```{language}\n")
            md_file.write(content)
            md_file.write("\n```\n\n")
    
    print(f"Markdown generation complete: {output_file}")

def get_language_from_extension(extension):
    """Map file extension to markdown code language."""
    extension_map = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'html': 'html',
        'css': 'css',
        'c': 'c',
        'cpp': 'cpp',
        'cs': 'csharp',
        'java': 'java',
        'rb': 'ruby',
        'php': 'php',
        'go': 'go',
        'rs': 'rust',
        'sh': 'bash',
        'md': 'markdown',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        'sql': 'sql',
        'kt': 'kotlin',
        'swift': 'swift',
        'dart': 'dart',
        'r': 'r',
        'jl': 'julia',
        'pl': 'perl',
        'lua': 'lua',
        'ex': 'elixir',
        'exs': 'elixir',
    }
    
    return extension_map.get(extension.lower(), '')

def main():
    parser = argparse.ArgumentParser(description='Generate a context document for a project.')
    parser.add_argument('project_dir', help='Path to the project directory')
    parser.add_argument('--name', help='Project name (defaults to directory name)')
    parser.add_argument('--output', help='Output file path or directory (if directory, a file with default name will be created)')
    parser.add_argument('--format', choices=['pdf', 'md'], default='pdf', help='Output format: pdf or md (markdown)')
    
    args = parser.parse_args()
    
    # Validate and process project directory
    project_dir = os.path.abspath(args.project_dir)
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a valid directory")
        return
    
    # Get project name
    project_name = args.name if args.name else os.path.basename(project_dir)
    
    # Get output format
    output_format = args.format
    
    # Determine file extension based on format
    file_extension = 'pdf' if output_format == 'pdf' else 'md'
    
    # Process output path
    if args.output:
        output_path = os.path.abspath(args.output)
        
        # Check if output is a directory
        if os.path.isdir(output_path) or output_path.endswith(os.sep):
            # Create directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, f"{project_name}_context.{file_extension}")
        elif os.path.isdir(os.path.dirname(output_path)) or not os.path.dirname(output_path):
            # Output is a file path with existing directory
            output_file = output_path
            # Create parent directory if needed
            parent_dir = os.path.dirname(output_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
        else:
            # Output is a file path with non-existing directory
            parent_dir = os.path.dirname(output_path)
            os.makedirs(parent_dir, exist_ok=True)
            output_file = output_path
    else:
        # Default: create in current directory
        output_file = f"{project_name}_context.{file_extension}"
    
    # Ensure the file has the correct extension
    if not output_file.lower().endswith(f".{file_extension}"):
        output_file += f".{file_extension}"
    
    print(f"Generating context {output_format.upper()} for project: {project_name}")
    print(f"Scanning directory: {project_dir}")
    print(f"Output file: {output_file}")
    
    if output_format == 'pdf':
        generate_pdf(project_name, project_dir, output_file)
        print(f"PDF generation complete: {output_file}")
    else:  # markdown
        generate_markdown(project_name, project_dir, output_file)
        print(f"Markdown generation complete: {output_file}")

if __name__ == "__main__":
    main()