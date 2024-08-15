import csv
import os

from flask import Flask
from flask import request, Response

# create Flask app instance
app = Flask(__name__)

# get the value of the environment variable named "DATA"
data = os.environ.get("DATA", "..")

# define a handler for the root URL "/"
@app.route("/", methods=["GET", "POST"])
def homepage():
    return "Hi there, how ya doin?"

# define a handler for the "/sum_calculator" endpoint
@app.route("/sum_calculator", methods=["POST"])
def sum_calculator():
    # get the JSON data from the request
    request_data = request.get_json()
    try:
        # get the file name and the product name from the JSON data
        file = data + "/" + request_data["file"]
        product = request_data["product"]
    except KeyError:
        # handle error if the JSON data is invalid
        return Response(
            '{"file": "null", "error": "Invalid JSON input."}',
            status=400
        )

    try:
        # check if the file is in the expected CSV format
        if not file_validator(file):
            raise ValueError
        else:
            # open the file and calculate the sum of the product column
            with open(file, mode="r") as dat_file:
                csv_file = csv.reader(dat_file)
                product_sum = 0
                for row in csv_file:
                    if product in row:
                        product_sum = product_sum + int(row[1])
                dat_file.close()

                # return the sum of the product column in a JSON response
                return Response(
                    '{"file": "%s", "sum": "%s"}' % (request_data["file"], product_sum),
                    status=200
                )

    except ValueError:
        # handle error if the file is not in CSV format
        return Response(
            '{"file": "%s", "error": "Input file not in CSV format."}'
            % request_data["file"],
            status=415
        )

    except FileNotFoundError:
        # handle error if the file is not found
        return Response(
            '{"file": "%s", "error": "File not found."}' % request_data["file"],
            status=404
        )


# function to validate if the CSV file is in expected format
def file_validator(file):
    with open(file, mode="r") as dat_file:
        csv_file = csv.reader(dat_file, skipinitialspace=True,quoting=csv.QUOTE_ALL)
        expected_header = ['product', 'amount']
        
        header = next(csv_file)
        # Remove whitespace from each field in the header row
        processed_header = [field.strip() for field in header]

        if processed_header != expected_header:
            return False
        else:
            # Check if every row in the CSV file has the same number of columns as the header row
            for row in csv_file:
                if len(row) != len(header):
                    return False
            return True


# start the Flask app
if __name__ == "__main__":
    hostname = os.environ.get("HOSTNAME", "0.0.0.0")
    # run the app with the given host and port number
    app.run(host=hostname, port=9878)
