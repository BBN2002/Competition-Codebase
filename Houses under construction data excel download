from flask import Flask, send_from_directory
import os

app = Flask(__name__)


@app.route('/download_excel')
def download_excel():
    # The directory path of the Excel file on the server
    directory_path = '/www/wwwroot/excel2/'
    filename = 'Houses under construction Data.xlsx'
    file_path = os.path.join(directory_path, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return send_from_directory(directory_path, filename, as_attachment=True)
    else:
        return "The file does not exist", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002,ssl_context=('/www/wwwroot/test/www.ksjzs.com.pem', '/www/wwwroot/test/www.ksjzs.com.key'))
