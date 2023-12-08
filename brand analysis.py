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
INPUT_DATA_FILENAME = 'Таблица Расшифровки.xlsx'
BRAND_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+BRAND_DATA_FILENAME
INPUT_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+INPUT_DATA_FILENAME

logging.debug(PATH_TO_CURRENT_DIR)


def main_algorith():
    brand_datatable = pd.read_excel(BRAND_DATA_FILENAME,)
    print(brand_datatable)
    logging.info(brand_datatable)



if __name__ == '__main__':
    print("START________________________________________")
    logging.debug("START________________________________________")
    main_algorith()
    logging.debug("FINISH_______________________________________")
    print("FINISH_______________________________________")
