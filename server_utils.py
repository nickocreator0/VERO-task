import numpy as np
import pandas as pd


def csv_to_json(csv_file):
    """
    :param csv_file: file storage returned as a response from server
    :return: json array of vehicle info
    """

    if csv_file is None:
        return 'No CSV file is transmitted'

    # Read CSV data
    df = pd.read_csv(csv_file, on_bad_lines='skip', delimiter=';')

    # Replace missing values (NAN) with None to match the missing value in resources
    df = df.replace({np.nan: None})

    # Create a dictionary with the records in csv
    records_dict = df.to_dict(orient='records')

    return records_dict


def filter_resources(resources):
    """
    Filters out the resources whose `hu` field is set to null
    :param resources: a list of dictionaries containing vehicle info obtained from server
    :return: a list of dictionaries containing vehicle info with Non-null values for the `hu` field
    """

    filtered_resources = []

    for resource in resources:
        if resource.get('hu') is not None:
            filtered_resources.append(resource)

    return filtered_resources


def store_all(csv_file, resources):
    """
    Stores both csv file and resources in an appropriate dictionary
    Takes care of the duplicates based on the field `kurzname`
    and returns distinct result.

    :param csv_file: json array containing vehicle info transmitted by client
    :param resources: json array of resources obtained from baubuddy
    :return: a list of dictionaries containing the API Response + request body
    """

    names_in_resources = []

    # Store all vehicle names present in resources
    for record in resources:
        names_in_resources.append(record['kurzname'])

    # Find the names of vehicles in csv file that don't exist in resources
    for record in csv_file:
        if record['kurzname'] not in names_in_resources:
            # Add a new record containing the new vehicle's info to resources
            resources.append(
                {key: record[key] if key in record.keys() else None for key in resources[0].keys()})

    # Add a key for colorCode
    for record in resources:
        record['colorCode'] = None

    return resources


def resolve_label_ids(label_ids):
    """
    Separates the ids in labelIds and returns them as items in a list.
    :param label_ids: a string containing potential ids
    :return: a list of ids
    """
    label_id_list = [str(label_id).strip() for label_id in str(label_ids).split(',')]

    return label_id_list


def resolve_color_code(vehicle_info, token):
    from external_request.server_request import get_color_code

    # Loop through records in vehicle info
    for record in vehicle_info:
        label_ids = record['labelIds']

        # Check if labelIds has a value
        if label_ids is not None:
            resolved_label_ids = resolve_label_ids(label_ids)

            # Request colorCode; only use the first labelId (the rest won't be required in this task)
            response = get_color_code(token=token, label_id=resolved_label_ids[0])

            # Extract colorCode from response
            color_code = response[0]['colorCode']

            # Store the colorCode in the data structure
            record['colorCode'] = color_code

    return vehicle_info
