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

def main():
    parser = argparse.ArgumentParser(description='Generate a PDF context document for a project.')
    parser.add_argument('project_dir', help='Path to the project directory')
    parser.add_argument('--name', help='Project name (defaults to directory name)')
    parser.add_argument('--output', help='Output PDF file path (defaults to project_name_context.pdf)')
    
    args = parser.parse_args()
    
    project_dir = os.path.abspath(args.project_dir)
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a valid directory")
        return
    
    # Get project name
    project_name = args.name if args.name else os.path.basename(project_dir)
    
    # Get output file
    output_file = args.output if args.output else f"{project_name}_context.pdf"
    
    print(f"Generating context PDF for project: {project_name}")
    print(f"Scanning directory: {project_dir}")
    print(f"Output file: {output_file}")
    
    generate_pdf(project_name, project_dir, output_file)
    print(f"PDF generation complete: {output_file}")

if __name__ == "__main__":
    main()