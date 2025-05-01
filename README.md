# CodeContext

   CodeContext is a lightweight Python tool that extracts the structure and content of your codebase into a single, well-formatted PDF or Markdown document. Perfect for sharing your entire project context with AI assistants like Claude or GPT, it helps you get more accurate and contextual help with your code. Simply point it to your project directory, and CodeContext automatically creates a comprehensive document containing your project's structure and all source files while intelligently excluding binaries, media, and other non-essential files. Improve your AI coding assistance with complete project context at your fingertips.


## Features

- **Complete Project Structure**: Displays a tree view of your project's directory structure
- **Full Code Extraction**: Includes the content of all relevant source code files
- **Multiple Output Formats**: Generate documentation in PDF or Markdown format
- **Syntax Highlighting**: Applies appropriate language-specific syntax highlighting in Markdown output
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

### Basic Usage

Generate a PDF document with default options:
```bash
python main.py /path/to/your/project
```

Generate a Markdown document:
```bash
python main.py /path/to/your/project --format md
```

### Command Line Options

```bash
python main.py /path/to/your/project [--name PROJECT_NAME] [--output OUTPUT_FILE]
```

#### Required Arguments:
- `project_dir`: Path to the project directory you want to document

#### Optional Arguments:
- `--name`: Custom project name (defaults to directory name)
- `--output`: Output file path or directory (will create directories if they don't exist)
- `--format`: Output format, either `pdf` or `md` (default is `pdf`)

### Examples

Generate a PDF with default name in the current directory:
```bash
python main.py ~/projects/my-flask-app
```

Generate a Markdown file with a custom project name:
```bash
python main.py ~/projects/my-flask-app --name "Flask Application" --format md
```

Specify an output directory (will be created if it doesn't exist):
```bash
python main.py ~/projects/my-flask-app --output ~/documents/code_docs/
```

Specify a complete output file path:
```bash
python main.py ~/projects/my-flask-app --name "Flask Application" --output flask_app_context.pdf
```

## Output Examples

### PDF Output

The PDF output includes:
1. **Title Page**: Contains the project name
2. **Project Structure**: A tree-view representation of your project's directory structure
3. **Source Code**: Each file is presented with:
   - Relative file path (e.g., `src/main.py`)
   - Full file content in a formatted code block


### Markdown Output

The Markdown output includes:
1. **Title**: Project name as main heading
2. **Project Structure**: A tree-view representation in a code block
3. **Source Code**: Each file is presented with:
   - Relative file path as a subheading
   - Full file content in a syntax-highlighted code block based on the file type


## What's Excluded?

The generator automatically excludes:
- **Binary files**: Images, videos, audio, etc.
- **Git-related content**: `.git` directory and files like `.gitignore`
- **Compiled files**: `.pyc`, `.exe`, etc.
- **Document files**: `.pdf`, `.doc`, etc.
- **Archives**: `.zip`, `.tar`, etc.

## Why Use CodeContext?

When working with AI assistants like Claude, GPT, etc., providing full context of your project helps the AI understand your codebase better. This tool creates a single, well-formatted document that you can upload to these services for more accurate and relevant assistance.

Benefits include:
- **Better AI Understanding**: LLMs can see your entire project structure and code together
- **Improved Assistance**: Get more accurate help with debugging, refactoring, and feature additions
- **Easier Collaboration**: Share your project context with team members or mentors
- **Documentation**: Quickly generate readable documentation of your codebase

## Requirements

- Python 3.6+
- ReportLab library (for PDF generation)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Roadmap

- [x] PDF output support
- [x] Markdown output support
- [ ] HTML output support
- [ ] Custom theme options
- [ ] Advanced syntax highlighting
- [ ] Inclusion/exclusion patterns
- [ ] Documentation summarization using AI

## Credits

Created by [Eiadur Rahman](https://github.com/EiadurRahman)