from argparse import ArgumentParser
import os

if __name__ == '__main__':
    from external_request.client_request import transmit_csv
    from client_utils import generate_excel

    # Get the JSON data structure from server
    server_response = transmit_csv("vehicles.csv")
    parser = ArgumentParser()

    # Get a list of column names
    parser.add_argument('-k', '--keys', nargs='+')

    # Get the boolean determining whether the conditional coloring should be applied
    parser.add_argument('-c', '--colored', action='store_true')
    args = parser.parse_args()

    filename = generate_excel(server_response, args.keys, args.colored)
