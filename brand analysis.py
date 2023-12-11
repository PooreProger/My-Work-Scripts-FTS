import os
import logging
import pandas as pd

logging.basicConfig(
    level=logging.DEBUG, 
    filename="brand logz.log", 
    encoding='utf-8', 
    format='%(asctime)s %(levelname)s %(message)s')


PATH_TO_CURRENT_DIR = os.getcwd()
BRAND_DATA_FILENAME = 'Бренды под АВР.xlsx'
INPUT_DATA_FILENAME = 'Таблица ввода данных.xlsx'
BRAND_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+BRAND_DATA_FILENAME
INPUT_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+INPUT_DATA_FILENAME

logging.debug(PATH_TO_CURRENT_DIR)


def main_algorith():
    logging.debug("Loading datasheets...")
    brand_datatable = pd.read_excel(BRAND_DATA_FILENAME)
    logging.info(f"Brand sheet:\n{brand_datatable}")
    input_datatable = pd.read_excel(INPUT_DATA_FILENAME)
    logging.info(f"Input sheet:\n{input_datatable}")
    logging.debug("Datasheets loaded.")

    logging.debug("Clearing data...")
    brand_datatable.iloc[:, 1] = brand_datatable.iloc[:, 1].astype(str)
    brand_datatable.iloc[:, 2] = brand_datatable.iloc[:, 2].astype(str)
    brand_datatable.iloc[:, 3] = brand_datatable.iloc[:, 3].astype(str)
    logging.debug("Data've been cleared.")

    logging.debug("Analyzing data...")
    for brandDT_RowIndex in brand_datatable.index:
        brand_main_name = None
        brand_second_name = None
        brand_list_of_currupted_names = [None]
        brand_names = []
        if brand_datatable.iat[brandDT_RowIndex, 1] != "nan":
            brand_main_name = brand_datatable.iat[brandDT_RowIndex, 1]
        if brand_datatable.iat[brandDT_RowIndex, 2] != "nan":
            brand_second_name = brand_datatable.iat[brandDT_RowIndex, 2]
        if brand_datatable.iat[brandDT_RowIndex, 3] != "nan":
            brand_list_of_currupted_names = brand_datatable.iloc[brandDT_RowIndex, 3].split(",")
        brand_names = [brand_main_name, brand_second_name]
        brand_names.extend(brand_list_of_currupted_names)
        logging.debug(f"\nMain name: {brand_main_name}\nSecond name: {brand_second_name}\nCurrpted names: {brand_list_of_currupted_names}\n{brand_names}")

       
    logging.debug("Analysis done.")





if __name__ == '__main__':
    print("STARTING________________________________________")
    logging.debug("START________________________________________")
    main_algorith()
    logging.debug("FINISH_______________________________________")
    print("FINISH_______________________________________")
