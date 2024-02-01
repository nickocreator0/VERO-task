from datetime import datetime
import pandas as pd


def form_columns(df, keys):
    """
    Forms a new dataframe where column names are taken from input
    The field `rnr` is included whether entered by user or not
    :param df: dataframe containing vehicle info
    :param keys: a list of strings containing column names requested by client
    :return: a new dataframe with the columns in inputs + `rnr`
    """
    # Columns should include the `rnr` field
    columns = []

    # Include additional columns if they match with the keys present in `df`
    for col in df.columns:
        if col != 'rnr' and col not in keys:
            pass
        else:
            columns.append(col)

    user_specified_df = df[columns]

    return user_specified_df


def conditional_formatting(df, user_specified_df, input_col_names, colored):
    """
    Takes care of tinting and coloring based on the requirements given in README file
    :param df:
    :param user_specified_df:
    :param input_col_names:
    :param colored:
    :return:
    """
    # Get the ISO-formatted current date
    current_date = datetime.now()

    # Create a file with the specified name
    excel_filename = f'vehicles_{current_date.isoformat()[0:10]}.xlsx'

    # Instantiate an object to write to the excel file
    excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

    # Write the new dataframe to the excel file
    user_specified_df.to_excel(excel_writer)

    # Check if `labelIds` is in the input arguments
    if 'labelIds' in input_col_names:
        color = excel_writer.book.add_format()

        # Loop through the rows in df
        for i, row in df.iterrows():
            # Check if the colorCode has been resolved
            if row['colorCode'] is not None:
                color.set_font_color(row['colorCode'])

                # Tint the text in corresponding row in `labelIds`
                excel_writer.sheets['Sheet1'].write(i + 1,
                                                    df.columns.get_loc('labelIds') + 1,
                                                    row['labelIds'],
                                                    color)

    # Check if -c is True and format based on the field `hu`
    if colored:
        for i, row in df.iterrows():
            hu_date = datetime.strptime(row['hu'], '%Y-%m-%d').date()
            now = current_date.date()

            if (now - hu_date).days < 90:
                color = '#007500'  # Green
            elif (now - hu_date).days < 365:
                color = '#FFA500'  # Orange
            else:
                color = '#b30000'  # Red

            # Use the color for formatting the cells
            cell_format = excel_writer.book.add_format({'bg_color': color})
            excel_writer.sheets['Sheet1'].set_row(i + 1, cell_format=cell_format)

    excel_writer.close()

    return excel_filename


def generate_excel(server_response, keys, colored):
    """
    Converts the vehicle info, converts it to an excel file, and saves it in the project's root directory
    :param server_response:
    :param keys:
    :param colored:
    :return:
    """
    # Convert the server response to pandas dataframe
    df = pd.DataFrame(server_response)

    # Sort rows by the field `gruppe`
    df = df.sort_values(by='gruppe')

    # Generate a new dataframe with user-specified columns
    user_specified_df = form_columns(df, keys)

    # Resolve cell colors
    filename = conditional_formatting(df=df, user_specified_df=user_specified_df,
                                      input_col_names=keys, colored=colored)

    return filename
