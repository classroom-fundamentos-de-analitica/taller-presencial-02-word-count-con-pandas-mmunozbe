"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    filenames = glob.glob(input_directory + '/*.*')
    dataframes = [pd.read_csv(file, sep = ";", names=["text"]) for file in filenames]
    dataframes = pd.concat(dataframes).reset_index(drop=True)
    return dataframes



def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.lower().str.replace(",", '').str.replace(".", '')
    return dataframe


def count_words(dataframe):
    """Word count"""
    #
    # Cuente el número de palabras en cada línea del DataFrame.
    #
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.split()
    dataframe = dataframe.explode('text').reset_index(drop=True)
    dataframe = dataframe.rename(columns = {'text':'word'})
    dataframe['value'] = 1
    conteo = dataframe.groupby(['word'], as_index=False).agg({'value':'sum'})
    return conteo
    


def save_output(dataframe, output_filename):
    """Save output to a file."""
    #
    # Guarde el conteo de palabras en el archivo output_filename.
    #
    dataframe.to_csv(output_filename, index=False, sep="\t", header=False)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    datafrane = load_input(input_directory)
    datafrane = clean_text(datafrane)
    datafrane = count_words(datafrane)
    save_output(datafrane, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
