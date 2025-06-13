import re
import sys
import pandas as pd

def parse_runs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    runs = []
    current_run = {}
    run_number_pattern = re.compile(r'^(\d+),,,')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is the run number line (title line at end of run)
        match = run_number_pattern.match(line)
        if match:
            # Current run finished, assign run number and save
            current_run['RUN'] = int(match.group(1))
            runs.append(current_run)
            current_run = {}  # Reset for next run
        elif '=' in line:
            # Parse parameter line: "param = value, error, error,\"
            try:
                param, vals = line.split('=', 1)
                param = param.strip()
                vals = vals.strip().rstrip('\\').strip()
                value_str = vals.split(',')[0].strip()
                current_run[param] = float(value_str)
            except Exception as e:
                print(f"Warning: skipping line due to parse error: {line}\n  Error: {e}")

    return runs

def runs_to_dataframe(runs):
    # Convert list of dicts to DataFrame, sorting columns for neatness
    df = pd.DataFrame(runs)
    df = df.reindex(sorted(df.columns), axis=1)
    return df

def main(input_file):
    print(f"Parsing file: {input_file}")
    runs = parse_runs(input_file)
    df = runs_to_dataframe(runs)

    output_csv = input_file.rsplit('.', 1)[0] + '_parsed.csv'
    df.to_csv(output_csv, index=False)

    print(f"Output saved to: {output_csv}")
    print(f"Total runs extracted: {len(runs)}")
    print(f"Available columns: {list(df.columns)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_datafile.py <input_file>")
    else:
        main(sys.argv[1])

#USAGE 
#Navigate to the directory of the host folder of this script in command prompt
#then run:
#python parse_datafile.py datafile.txt
#ensuring that the datafile.txt is the correct one you want to parse through
#and ensuring there is no alreayd parsed datafile in the folder, it will not overwrite a previous one
#so rename the previous one and it should create a new one called
#datafile_parsed.csv
#It will also display all the columns in the command line, if it does not try resaving every script. 