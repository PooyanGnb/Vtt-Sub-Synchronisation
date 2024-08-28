# Flask Subtitle Processing API

This Flask application provides an API to upload movie subtitle files in VTT format, synchronize them, and download the results as a CSV file. It supports uploading two subtitle files at a time, one for each language, and outputs a CSV file with timestamps and synchronized subtitles from both languages.

## Features

- Upload two VTT subtitle files.
- Synchronize subtitles based on timestamps.
- Download a CSV file containing synchronized subtitles.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7+
- pip (Python package installer)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/PooyanGnb/Vtt-Sub-Synchronisation
   cd Vtt-Sub-Synchronisation
   ```

2. **Set Up a Virtual Environment** (Optional but recommended)

   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS and Linux:
   source venv/bin/activate
   ```

3. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the application, run:

```bash
python main.py
```

This will start the Flask server on `http://127.0.0.1:5000/`. The API is now ready to receive requests.

## API Usage

### Endpoint: Upload and Synchronize Subtitles

- **URL**: `/sync`
- **Method**: `POST`
- **Body** (form-data):

	| key | type | Required |
	|----|----|----|
	| first_file | file(vtt) | Required
	| second_file | file(vtt) | Required

### How to Use

1. **Prepare Your Subtitle Files**: Ensure you have two subtitle files in VTT format that you want to synchronize.

2. **Use a Tool Like Postman**:
   - Set the method to `POST`.
   - Set the URL to `http://127.0.0.1:5000/api/upload`.
   - In the Body section, switch to form-data.
   - Add two files with the keys `first_file` and `second_file`.
   - Send the request.

3. **Download the Result**:
   - Upon successful processing, the API will return a CSV file as a download.
   - The file will contain three columns: Time, First (subtitle text from `first_file`), Second (subtitle text from `second_file`).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Pooyan Ghanbari - [linkedin](https://www.linkedin.com/in/pooyan-ghanbari/) 

Project Link: [https://github.com/PooyanGnb/Vtt-Sub-Synchronisation](https://github.com/PooyanGnb/Vtt-Sub-Synchronisation)
