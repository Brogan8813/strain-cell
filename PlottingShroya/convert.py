import pandas as pd
from glob import glob
import os
import csv
import numpy as np
import math as ma

mass_err = 0.01/1000  # Mass error constant
Avogadro_num = 6.0221409*10**(23)
Bohr_mu = 9.27400994*10**(-24)

def convert_magnetomerty_data(experiment, file):
    """
    Converts raw magnetometry data into a structured format, computes relevant properties, 
    and saves the output as a CSV file.
    
    Parameters:
        experiment (dict): Experiment details including mass and type.
        file (str): Path to the data file.
    
    Returns:
        DataFrame: Processed data.
    """
    headers, data, ext = read_data(file)
    if ext == ".dat":
        df = process_dat_file(experiment, headers, data)
    elif ext == ".txt":
        df = process_txt_format(experiment, headers, data, file)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    output = file.lower().replace(ext, '.csv')
    df.to_csv(output)
    return df

def app(experiment, files=None):
    """
    Main function to process multiple magnetometry data files.
    
    Parameters:
        experiment (dict): Experiment details including mass and type.
        files (list, optional): List of file paths to process. Defaults to None.
    """
    if files is not None:
        for file in files:
            convert_magnetomerty_data(experiment, file)
    elif len(experiment['files']) > 0:
        for file in experiment['files']:
            convert_magnetomerty_data(experiment, file)
    else:
        files = glob("*.dat")  # Process all .dat files in directory
        for file in files:
            convert_magnetomerty_data(experiment, file)
    return

def read_data(file):
    """
    Reads magnetometry data files of various formats (.dat, .txt, .fld).
    
    Parameters:
        file (str): Path to the file.
    
    Returns:
        tuple: (headers, data, file extension)
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"File '{file}' not found.")
    
    name, ext = os.path.splitext(file)
    ext = ext.lower()  # Normalize extension for case insensitivity
    
    # Define settings based on file type
    if ext == ".dat":
        header_num, sub_header_num, delimiter = 30, 0, ","
    elif ext == ".txt":
        header_num, sub_header_num, delimiter = 1, 0, "\t"
    elif ext == ".fld":
        header_num, sub_header_num, delimiter = 2, 3, " "
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    try:
        with open(file, "r") as f:
            reader = csv.reader(f, delimiter=delimiter)
            lines = list(reader)
            
            if len(lines) <= header_num:
                raise ValueError(f"File '{file}' does not contain enough lines for headers.")
            
            headers = lines[header_num]  # Extract headers
            data = lines[header_num + sub_header_num + 1:]  # Extract data rows
            
            if not data:
                raise ValueError(f"File '{file}' contains no data after headers.")
            
            # Ensure all rows have the same length
            max_len = max(len(row) for row in data)
            data = [row + [0]*(max_len - len(row)) for row in data]
            
            data = np.asarray(data, dtype=object)  # Preserve strings
            return headers, data, ext
    except Exception as e:
        print(f"Error reading file: {e}")
        return headers, data, ext

def get_index(headers, name):
    """Safely get the index of a column in headers. Returns None if not found."""
    try:
        return headers.index(name)
    except ValueError:
        return None

def process_dat_file(experiment, headers, data):
    """
    Processes .dat files from SQUID magnetometry experiments.
    
    Parameters:
        experiment (dict): Experiment details including type, mass, and molecular mass.
        headers (list): Column headers from data file.
        data (numpy array): Data extracted from the file.
    
    Returns:
        DataFrame: Processed magnetometry data.
    """
    # Define possible column names
    possible_columns = {
        "time": ["Time", "Time Stamp (sec)"],
        "temp": ["Temperature (K)"],
        "mo": ["Long Moment (emu)", "Moment (emu)"],
        "mo_err": ["Long Scan Std Dev", "M. Std. Err. (emu)"],
        "field": ["Field (Oe)", "Magnetic Field (Oe)"]
    }
    
    # Get the actual indices
    indices = {key: None for key in possible_columns}
    for key, col_names in possible_columns.items():
        for name in col_names:
            idx = get_index(headers, name)
            if idx is not None:
                indices[key] = idx
                break
    
    # Ensure required indices exist
    required_keys = ["time", "temp", "mo", "mo_err", "field"]
    if any(indices[key] is None for key in required_keys):
        raise ValueError("Missing required headers in the dataset.")
    
    mass = experiment['mass']
    mol_mass = experiment['mol_mass']
    
    # Convert data to numeric DataFrame
    df = pd.DataFrame({
        'Time': pd.to_numeric(data[:, indices["time"]], errors='coerce'),
        'Temperature(K)': pd.to_numeric(data[:, indices["temp"]], errors='coerce'),
        'Field(Oe)': pd.to_numeric(data[:, indices["field"]], errors='coerce'),
        'Field(T)': 0,
        'Long Moment(emu)': pd.to_numeric(data[:, indices["mo"]], errors='coerce'),
        'Long err': pd.to_numeric(data[:, indices["mo_err"]], errors='coerce')
    })
    
    df['Field(T)'] = df['Field(Oe)'] / 10000
    
    # Process based on experiment type
    if experiment['type'] == 'MvT':
        df['Susceptibility(m^3/mol)'], df['err'] = converttoChi(
            df["Long Moment(emu)"], df["Field(Oe)"], mass, mol_mass, err=df['Long err'], mass_err=mass_err
        )
    elif experiment['type'] == 'MvH':
        df['Magnetic moment(mu_b/n_fu)'], df['err'] = converttoMoment(
            df["Long Moment(emu)"], mass, mol_mass, err=df['Long err'], mass_err=mass_err
        )
    
    return df


def process_txt_format(experiment, headers, data, filename):
    # for 2 coloumn data in .txt format from squid lab
    lenth = len(data[:, 0])
    df = pd.DataFrame({ 'Time' : [0]*lenth,
                    'Temperature(K)' : [0]*lenth,
                    })
    
    mass = experiment['mass']
    mol_mass = experiment['mol_mass']

    if experiment['type'] == 'MvT':
        field_val = toFloat(filename.split("_")[2]) # Get field val form file name
        df['Temperature(K)'] = data [:, 0].astype(np.float)
        df['Field(Oe)'] = field_val
        df['Long Moment(emu)'] = data [:, 1].astype(np.float)
        df['Susceptibility(m^3/mol)'], df['err'] = converttoChi(
            df['Long Moment(emu)'], field_val, mass, mol_mass, mass_err=mass_err)
    elif experiment['type'] == 'MvH':
        #df['Temperature(K)'] = toFloat(filename.split("_")[2])
        df['Field(Oe)'] = data [:, 0].astype(np.float)
        df['Long Moment(emu)'] = data [:, 1].astype(np.float)
        df['Magnetic moment(mu_b/n_fu)'], df['err'] = converttoMoment(
            df['Long Moment(emu)'], mass, mol_mass, mass_err=mass_err)
    return df


def converttoMoment(value, mass, mol_mass, mass_err = 0.01/1000, err=0):

    #covert mag_moment units
    n_fu = Avogadro_num*mass/mol_mass

    mu_Am2 = value*10**(-3)
    mu = (mu_Am2/Bohr_mu)*(1/n_fu)
    mu_error = error_propagator(value, err, mass, mass_err, mu)

    #mu = np.stack((mu, mu_error), axis = 1)
    return mu, mu_error

def converttoChi(value, field, mass, mol_mass, mass_err = 0.01/1000, err=0):

    # converts magmoment to chi

    n_mol = mass/mol_mass
    chi_emu = (value/field)*(1/n_mol)

    chi = chi_emu*4*ma.pi*10**(-6)
    chi_error = error_propagator(value, err, mass, mass_err, chi)

    #chi = np.stack((chi, chi_error), axis = 1)
    return chi, chi_error

def error_propagator(x, err_x, y, err_y, Z):
    err = abs(Z*np.sqrt((err_x/x)**2 + (err_y/y)**2))
    return err

def toFloat(value):
    try:
        value = float(value)
    except ValueError:
        pass
    return value
