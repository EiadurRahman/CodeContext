# CodeContext

A Python tool that extracts code from your project and creates a comprehensive PDF document containing your project's structure and source code. This makes it easy to share your entire project context with LLMs like Claude for better understanding and assistance.

## Features

- **Complete Project Structure**: Displays a tree view of your project's directory structure
- **Full Code Extraction**: Includes the content of all relevant source code files
- **Excludes Unnecessary Files**: Automatically filters out binary files, media assets, and Git-related content
- **Clean Formatting**: Organizes content with proper headings, code blocks, and spacing
- **Simple CLI Interface**: Easy to use with customizable options

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/EiadurRahman/CodeContext.git
   cd CodeContext
   ```

2. Install the required dependencies:
   ```bash
   pip install reportlab
   ```

## Usage

Basic usage with default options:

```bash
python main.py /path/to/your/project
```

This will:
1. Scan the specified project directory
2. Create a PDF named `[directory_name]_context.pdf` in the current directory

### Command Line Options

```bash
python mainr.py /path/to/your/project [--name PROJECT_NAME] [--output OUTPUT_FILE]
```

- `project_dir`: Path to the project directory (required)
- `--name`: Custom project name (defaults to directory name)
- `--output`: Custom output file path (defaults to project_name_context.pdf)

## Example

```bash
python main.py ~/projects/my-flask-app --name "Flask Application" --output flask_app_context.pdf
```

## What's Included in the PDF?

1. **Title Page**: Contains the project name
2. **Project Structure**: A tree-view representation of your project's directory structure
3. **Source Code**: Each file is presented with:
   - Relative file path (e.g., `src/main.py`)
   - Full file content in a code block

## What's Excluded?

The generator automatically excludes:

- **Binary files**: Images, videos, audio, etc.
- **Git-related content**: `.git` directory and files like `.gitignore`
- **Compiled files**: `.pyc`, `.exe`, etc.
- **Document files**: `.pdf`, `.doc`, etc.
- **Archives**: `.zip`, `.tar`, etc.

## Why Use This Tool?

When working with AI assistants like Claude, GPT, etc., providing full context of your project helps the AI understand your codebase better. This tool creates a single, well-formatted PDF that you can upload to these services for more accurate and relevant assistance.

## Requirements

- Python 3.6+
- ReportLab library

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# MarkDown support comming soon!
