import os
import socket
import requests

from flask import Flask
from flask import request, Response

# Create a Flask app
app = Flask(__name__)

# Get the value of the HOSTNAME environment variable or default to "127.0.0.1"
hostname = os.environ.get("HOSTNAME", "127.0.0.1")

# Get the value of the DATA environment variable or default to an empty string
data = os.environ.get("DATA", "..")


@app.route("/", methods=["GET", "POST"])
@app.route("/start", methods=["GET", "POST"])
def start():
    # Get the IP address of the current host operating system
    external_ip = socket.gethostbyname(socket.gethostname())

    # Return a response with a JSON payload containing a banner and the external IP address
    return Response('{ "banner": "B00947059","ip": "' + external_ip + '"}',
                    mimetype="application/json",
                    status=200)


@app.route("/store-file", methods=["POST"])
def store_file():
    request_data = request.get_json()
    try:
        # If the "file" key is missing from the JSON payload, raise a KeyError
        if request_data["file"] == "" or type(request_data["file"]) == type(None):
            raise KeyError
        else:
            # Split the data by newline
            lines = request_data["data"].split("\n")

            # Open the file specified in the JSON payload and write each line to it
            with open(data + "/" + request_data["file"], "w") as file:
                for line in lines:
                    file.write(line + "\n")
                
                file.close()
            
            # Return a response with a JSON payload indicating a successful file storage
            return Response('{"file": "%s", "message": "Success."}' % request_data["file"],
                            mimetype="application/json",
                            status=200)
    except KeyError:
        # If a KeyError was raised, return an error message with a 400 status code
        return Response('{"file": null, "error": "Invalid JSON input."}',
                        mimetype="application/json",
                        status=400)
    except OSError:
        # If an OSError was raised, return an error message with a 400 status code
        return Response('{"file": "file.dat", "error": "Error while storing the file to the storage."}',
                        mimetype="application/json",
                        status=400)


@app.route("/calculate", methods=["POST"])
def calculate():
    request_data = request.get_json()
    try:
        # If the "file" key is missing from the JSON payload, raise a KeyError
        if request_data["file"] == "" or type(request_data["file"]) == type(None):
            raise KeyError
        # If the file specified in the "file" key does not exist, raise a FileNotFoundError
        elif not os.path.exists(data + "/" + request_data["file"]):
            raise FileNotFoundError
        else:
            # Send a POST request to another service to calculate the sum of the file contents
            resp = requests.post("http://" + hostname + ":9878/sum_calculator", json=request_data)
            # Return the response from the other service with the appropriate status code and MIME type

            return Response(resp.text,
                            mimetype="application/json",
                            status=resp.status_code)
    except KeyError:
        # If a KeyError was raised, return an error message with a 400 status code
        return Response('{"file": null, "error": "Invalid JSON input."}',
                        mimetype="application/json",
                        status=400)
    except FileNotFoundError:
        # If a FileNotFoundError was raised, return an error message with a 404 status code
        return Response('{"file": "%s", "error": "File not found."}' % request_data["file"],
                        mimetype="application/json",
                        status=404)


@app.errorhandler(500)
@app.errorhandler(400)
def internal_error():
    # Return a generic error message with a 400 status code for 500 and 400 error handlers
    return Response('{"file": null, "error": "Invalid JSON input."}',
                    mimetype="application/json",
                    status=400)


# Start the Flask app on port 6000 and allow connections from any IP address
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)