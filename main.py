from flask import Flask, request, jsonify, send_file
import os

from utils import *

# Initialize Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/sync', methods=['POST'])
def upload_files():
    """
    Flask endpoint to handle uploading of subtitle files and downloading the synchronized CSV.
    Returns:
        Response: A file download response containing the synchronized subtitles.
    """
    first_file = request.files.get('first_file')
    second_file = request.files.get('second_file')

    # Ensure both files are provided
    if not first_file or not second_file:
        return jsonify({"error": "Both subtitle files are required"}), 400  # Return an error if one or both files are missing

    # Save the uploaded files to the uploads directory
    first_path = os.path.join(app.config['UPLOAD_FOLDER'], first_file.filename)
    second_path = os.path.join(app.config['UPLOAD_FOLDER'], second_file.filename)
    first_file.save(first_path)
    second_file.save(second_path)

    # Process the VTT files to parse and align subtitles
    first_subs = parse_vtt(first_path)  # Parse the first subtitle file
    second_subs = parse_vtt(second_path)  # Parse the second subtitle file
    aligned_subs = align_subtitles(first_subs, second_subs)  # Align the parsed subtitles from both files

    # Export the aligned subtitles to a CSV file
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'synchronized_subtitles.csv')
    export_to_csv(aligned_subs, output_path) # Function to export data to CSV

    # Send the CSV file as a download response
    response = send_file(output_path, mimetype='text/csv', as_attachment=True)
    response.headers["Content-Disposition"] = f'attachment; filename="synchronized_subtitles.csv"'
    return response

if __name__ == '__main__':
    app.run(debug=True)
