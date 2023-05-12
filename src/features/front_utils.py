from io import BytesIO
import pandas as pd
from cryptography.fernet import Fernet

def df_to_excel_bytes(df, sheet_name='Sheet1'):
    """
    Convert a pandas DataFrame to an Excel file in memory and return the bytes-like object.
    """
    # create a BytesIO object
    excel_file = BytesIO()

    # create a Pandas Excel writer using the BytesIO object as the file
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        # write the DataFrame to a sheet in the Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # get the bytes-like object from the BytesIO object
    excel_file.seek(0)
    excel_bytes = excel_file.read()

    return excel_bytes

def import_encrypted_csv(file_path, key):
    # Create a Fernet instance with the key
    fernet = Fernet(key)

    # Load the encrypted data from file
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data and convert it back to a DataFrame
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    df = pd.read_csv(io.StringIO(decrypted_data))

    return df