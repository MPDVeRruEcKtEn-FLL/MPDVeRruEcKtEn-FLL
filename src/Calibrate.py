import numpy as np
import pandas as pd
import tkinter as tk

def generate_polynomial_functions(csv_file, output_file="regler_functions.py"):
    # CSV-Datei einlesen mit ; als Trennzeichen und , als Dezimaltrennzeichen
    df = pd.read_csv(csv_file, delimiter=';', decimal=',')
    
    if 'SPEED' not in df.columns:
        raise ValueError("CSV-Datei muss eine 'SPEED'-Spalte enthalten.")
    
    speed = df['SPEED'].values
    
    functions = {}
    
    for column in df.columns:
        if column != 'SPEED':
            coefficients = np.polyfit(speed, df[column].values, 6)
            
            function_str = "      + ".join(
                f"{coef:.15e}*speed**{6-i}\n" for i, coef in enumerate(coefficients)
            )
            
            functions[column] = f"""
def {column}_function(speed):
    return (\n      {function_str})
"""
    
    # Funktionen in Python-Datei speichern
    with open(output_file, "w") as f:
        f.write("\n".join(functions.values()))
    
    print(f"Funktionen wurden in {output_file} gespeichert.")

def calibrate_gui():
    root = tk.Tk()
    root.title = "PID-Calibration"

    frm = tk.Frame(root)
    frm.pack(fill = "both")

    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generiert Polynomfunktionen aus einer CSV-Datei.")
    parser.add_argument("csv_file", help="Pfad zur CSV-Datei")
    parser.add_argument("--output", default="regler_functions.py", help="Ausgabedatei für die Funktionen")
    args = parser.parse_args()
    
    generate_polynomial_functions(args.csv_file, args.output)
