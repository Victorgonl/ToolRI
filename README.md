# ToolRI

ToolRI was created to simplify and standardize the creation of samples for the task of Information Extraction in document images. The tool allows text extraction by OCR, the creation of document entities and their labeling and linking. The project was created purely with Python and can be run on any desktop platform. The graphical user interface is implemented thanks to the amazing <a href="https://github.com/tomschimansky/customtkinter">CustomTkinter</a> library.

## Instalation

### Pypi

Install the ToolRI package with `pip`:

    pip install toolri

### Source

Clone the ToolRI repository with:

    git clone https://github.com/Victorgonl/ToolRI

And install using `pip`:

    pip install ./ToolRI/

## Standalone

### Download

You can download a portable binary of the tool to start using right away. Download and run a version on the <a href="https://github.com/Victorgonl/ToolRI/releases">releases</a> page of the ToolRI repository.

### Build

To build the standalone version of ToolRI into a portable binary, clone the repository:

    git clone https://github.com/Victorgonl/ToolRI

Change current directory to `./ToolRI`:

    cd ./ToolRI

Install all the dependencies found on `requirements.txt`:

    pip install -r requirements.txt

And run the script `toolri_build.py`:

    python3 toolri_build.py

The binary will be available on `dist` folder.

## Documentation

***Under construction.*** :construction:

## Tesseract OCR

To be able to use the OCR function in ToolRI, Tesseract OCR must be installed separately.

***For now, OCR is configured for English and Portuguese languages only, but it will be updated soon for all languages available.*** :construction:

### Debian based

Use the command:

    sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-por

### Windows

- Download and run the installer available at https://github.com/UB-Mannheim/tesseract/wiki.

- Make sure to install Tesseract on `C:\Program Files\Tesseract-OCR\` (the default directory) due to a predefined configuration in current ToolRI version.

## Usage

ToolRI was developed and used to create the <a href="https://github.com/LabRI-Information-Retrieval-Lab/UFLA-FORMS">UFLA-FORMS</a> dataset. Download the dataset to try the tool on the available samples or create a new metadata for any document image available.

### Example

    import toolri

    image = toolri.load_image("document_image.jpg")

    labels = [
        toolri.ToolRILabel(name="QUESTION", color="#004B80", links=["ANSWER"], is_visible=True),
        toolri.ToolRILabel(name="ANSWER", color="#00943E", links=[], is_visible=True)
    ]

    data = toolri.toolri(image=image, data=data, labels=labels)

    toolri.draw_data_on_image(image=image, data=data, labels=labels).show()
