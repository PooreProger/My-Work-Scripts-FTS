import os
import logging
import pandas as pd
import re

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
    brand_datatable.iloc[:, 0] = brand_datatable.iloc[:, 0].astype(str)
    brand_datatable.iloc[:, 1] = brand_datatable.iloc[:, 1].astype(str)
    brand_datatable.iloc[:, 2] = brand_datatable.iloc[:, 2].astype(str)
    brand_datatable.iloc[:, 3] = brand_datatable.iloc[:, 3].astype(str)
    input_datatable['Сумма'] = input_datatable.iloc[:, 1:].sum(axis=1)
    # input_datatable.loc[input_datatable['Сумма'] != 0]
    logging.info(f"Input sheet summed without zeros:\n{input_datatable}")
    logging.debug("Data've been cleared.")

    logging.debug("Analyzing data...")
    for brandDT_RowIndex in brand_datatable.index:
        brand_names = []
        if brand_datatable.iat[brandDT_RowIndex, 0] != "nan":
            brand_main_name = brand_datatable.iat[brandDT_RowIndex, 0]
            brand_names.append(brand_main_name)
        if brand_datatable.iat[brandDT_RowIndex, 1] != "nan":
            brand_second_name = brand_datatable.iat[brandDT_RowIndex, 1]
            brand_names.append(brand_second_name)
        if brand_datatable.iat[brandDT_RowIndex, 2] != "nan":
            brand_currupted_names= brand_datatable.iloc[brandDT_RowIndex, 2]
            brand_list_of_currupted_names = brand_currupted_names.split(",")
            brand_names.extend(brand_list_of_currupted_names)
        logging.debug(f"Brand names:{brand_names}")

        for inputDT_RowIndex in input_datatable.index:
            isMatched = None
            matched_name = None
            input_brand_name = str(input_datatable.iat[inputDT_RowIndex, 0]).lower().strip()
            for brand_name in brand_names:
                brand_name = str(brand_name).lower().strip()
                isMatched = re.search(rf' {input_brand_name} ', fr' {brand_name} ')
                if isMatched is None:
                    isMatched = re.search(rf'\W{brand_name}\W', rf'\W{brand_name}\W')
                if isMatched:
                    matched_name = brand_main_name




        # for inputDT_RowIndex in input_datatable.index:
            
        # print(i for i in input_datatable(200:, index))
        # print(input_datatable(200:, index))

    print(input_datatable.index)



       
    logging.debug("Analysis done.")





if __name__ == '__main__':
    print("STARTING________________________________________")
    logging.debug("START________________________________________")
    main_algorith()
    logging.debug("FINISH_______________________________________")
    print("FINISH_______________________________________")
