import shutil
from os import getcwd
import os
from flask import Flask
from flask import request
from flask import send_file

from core import Core
from logging import getLogger

app = Flask(__name__)
log = getLogger(__name__)
core_object = Core()


@app.route("/", methods=["GET"])
def hello_world():
    """
    This is basic API status response.
    To check if application is running.
    :return:
    """
    message = {"message": "Hello World!!!"}
    return message


@app.route("/get_fasta", methods=["POST"])
def temp():
    """
    get multi-fasta file and return zip with with multiple genbank files.
    :return:
    """
    if request.method == "POST":
        f = request.files["file"]
        email = request.form["email"]
        meta = f"{getcwd()}"
        if not os.path.exists(f"{meta}\\fasta_files\\"):
            os.mkdir(f"{meta}\\fasta_files\\")
        file_path = f"{getcwd()}\\fasta_files\\{f.filename}"
        f.save(file_path)
        zip_file_path = core_object.convert_to_nucleotide(email=email,
                                                          file_path=file_path)
        print(zip_file_path)
        shutil.rmtree(f"{meta}\\fasta_files\\")
        shutil.rmtree(f"{meta}\\temp\\")
        shutil.rmtree(f"{meta}\\genbank\\")
        return send_file(zip_file_path,
                         attachment_filename="genbank_files.zip",
                         as_attachment=True)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
