from flask import Flask, request
from flask_cors import cross_origin
import json

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/getCsv', methods=['POST'])
@cross_origin()
def get_csv():
    from external_request.server_request import get_access_token, get_resources
    from server_utils import filter_resources, csv_to_json, store_all, resolve_color_code

    # Request csv file
    csv_file = request.files['file']

    json_csv = csv_to_json(csv_file)

    # Get access token
    access_token = get_access_token()

    # Request and get resources from baubuddy.de
    resources = get_resources(token=access_token)

    # Store both csv and resources in an appropriate dictionary
    combined_info = store_all(csv_file=json_csv, resources=resources)

    # Filter resources that don't have a value set for `hu` field
    filtered_combined_info = filter_resources(resources=combined_info)

    # Resolve the colorCodes
    info_color_resolved = resolve_color_code(vehicle_info=filtered_combined_info, token=access_token)

    return json.dumps(info_color_resolved)


if __name__ == '__main__':
    app.run(debug=True)
