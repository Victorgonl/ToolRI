# ToolRI

A tool for extracting, labeling and linking entities in document images for Information Extraction tasks.

## Important :warning:

ToolRI is under development and this is a prerelease of the tool. The tool will soon be updated and its source code will also be made publicly available along with its documentation.

## Running ToolRI

Download the executable for Linux or Windows in <a href="https://github.com/Victorgonl/ToolRI/releases">releases</a> <a></a> and run.

## Tesseract OCR

To be able to use the OCR function in ToolRI, Tesseract OCR must be installed separately. For the prerelease build, OCR is configured for English and Portuguese texts only.

### Debian based

Use the command:

    sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-por

### Windows

- Download and run the installer available at https://github.com/UB-Mannheim/tesseract/wiki.

- Make sure to install Tesseract on `C:\Program Files\Tesseract-OCR\` (the default directory) due to a predefined configuration in the prerelease build.

## Usage

ToolRI was created and used to label the <a href="https://github.com/LabRI-Information-Retrieval-Lab/UFLA-FORMS">UFLA-FORMS</a> dataset. Download the dataset to try the tool on the available samples or create a new metadata for any document image available.
