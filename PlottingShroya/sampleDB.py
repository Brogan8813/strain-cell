import os
import re
import json
import pandas as pd

def mol_mass_calc(formula):
    """
    Calculate the molecular mass of a compound from its chemical formula.
    
    This function uses an external CSV file ('elements.csv') containing the 
    atomic symbols and atomic masses of elements to compute the molecular 
    mass. The function parses the formula, retrieves the atomic mass for 
    each element in the formula, and sums the total molecular mass.

    Args:
        formula (str): The chemical formula of the compound (e.g., 'H2O').

    Returns:
        float: The calculated molecular mass of the compound.

    Raises:
        FileNotFoundError: If 'elements.csv' is missing or not found.
        ValueError: If the formula contains unknown elements or malformed data.
    """
    elements_file = os.path.abspath(os.path.join(os.getcwd(), "elements.csv"))
    
    # Check if the 'elements.csv' file exists
    if not os.path.exists(elements_file):
        raise FileNotFoundError("The 'elements.csv' file is missing!")

    # Read the elements database into a DataFrame
    db = pd.read_csv(elements_file)
    
    # Regular expression to split the formula into elements and numbers
    split = re.findall(r"[A-Z][a-z]?|[-+]?\d*\.?\d+", formula)
    molmass = 0  # Variable to accumulate the total molecular mass
    i = 0  # Iterator to parse through the split formula

    while i < len(split):
        element = split[i]  # Current element symbol
        num = 1  # Default to 1 if no number follows the element
        
        # Check if a number follows the element, indicating quantity
        if i + 1 < len(split) and re.match(r"[-+]?\d*\.?\d+", split[i + 1]):
            num = float(split[i + 1])  # Convert number to float
            i += 1  # Move to the next element

        # Search for the element in the database
        info = db.query('Symbol == @element')

        # Raise an error if element is not found in the database
        if info.empty:
            raise ValueError(f"Unknown element in formula: {element}")

        # Retrieve atomic mass for the element and update the molecular mass
        element_mass = info['AtomicMass'].values[0]
        molmass += num * element_mass
        i += 1

    return molmass

def read_sample_database(file="samplesDB.json"):
    """
    Reads the sample database JSON file and returns the data.
    
    This function loads the data from a JSON file containing sample information 
    and returns it as a Python dictionary.

    Args:
        file (str): The path to the JSON file (default is 'samplesDB.json').

    Returns:
        dict: The data loaded from the JSON file.

    Raises:
        FileNotFoundError: If the specified JSON file does not exist.
        ValueError: If there is an error decoding the JSON file.
    """
    # Check if the specified database file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"Database file '{file}' not found.")
    
    try:
        # Open the file and load the JSON data
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle errors related to malformed JSON
        raise ValueError("Error reading JSON file. Please check its format.")

def search_experiments(experiments, expID):
    """
    Searches for an experiment in a list of experiments by its unique ID.
    
    Args:
        experiments (list): A list of experiment dictionaries.
        expID (str): The unique ID of the experiment to search for.

    Returns:
        dict: The dictionary containing the experiment data.

    Raises:
        ValueError: If no experiment with the given ID is found.
    """
    # Loop through each experiment to find the one with the matching expID
    for exp in experiments:
        if exp["expID"] == expID:
            return exp  # Return the dictionary directly
    
    # Raise an error if experiment with given ID is not found
    raise ValueError(f"Experiment with ID '{expID}' not found.")

def search_samples(samples, batchNo):
    """
    Searches for a sample in the sample database by its batch number.
    
    Args:
        samples (list): A list of sample dictionaries.
        batchNo (str): The batch number of the sample to search for.

    Returns:
        dict: The dictionary containing the sample data.

    Raises:
        ValueError: If no sample with the given batch number is found.
    """
    # Loop through each sample to find the one with the matching batch number
    for sample in samples:
        if sample["batchNo"] == batchNo:
            return sample  # Return the dictionary directly
    
    # Raise an error if sample with given batch number is not found
    raise ValueError(f"Sample with batch number '{batchNo}' not found.")

def app(batchNo, expID):
    """
    Retrieves a sample and its corresponding experiment from the database.
    
    This function uses the batch number and experiment ID to look up the 
    relevant sample and experiment from a database. It also calculates the 
    molar mass of the sample based on its chemical formula.

    Args:
        batchNo (str): The batch number of the sample.
        expID (str): The experiment ID.

    Returns:
        tuple: A tuple containing the sample dictionary and the experiment dictionary.
    """
    # Load the sample database and search for the relevant sample
    samples = read_sample_database()
    sample = search_samples(samples, batchNo)
    
    # Search for the experiment in the sample's experiment list
    experiment = search_experiments(sample["experiments"], expID)

    # Convert mass from mg to grams
    experiment["mass"] = float(experiment["mass"]) / 1000
    
    # Ensure conditions is a list (split from a string if necessary)
    if isinstance(experiment["conditions"], str):
        experiment["conditions"] = experiment["conditions"].split(", ")
    
    # Calculate the molecular mass of the sample based on its formula
    experiment["mol_mass"] = mol_mass_calc(sample["formula"])
    
    # Return both the sample and the experiment data
    return sample, experiment
