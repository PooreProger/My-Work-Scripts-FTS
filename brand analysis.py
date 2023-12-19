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
OUTPUT_DATA_FILENAME = 'Вывод расшифрованных данных.xlsx'
BRAND_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+BRAND_DATA_FILENAME
INPUT_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+INPUT_DATA_FILENAME
OUTPUT_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+OUTPUT_DATA_FILENAME

logging.debug(PATH_TO_CURRENT_DIR)


def main_algorith():
    logging.debug("Loading datasheets...")
    brand_datatable = pd.read_excel(BRAND_DATA_FILENAME)
    logging.info(f"Brand sheet:\n{brand_datatable}")
    raw_input_datatable = pd.read_excel(INPUT_DATA_FILENAME)
    logging.info(f"Raw input sheet:\n{raw_input_datatable}")
    logging.debug("Datasheets loaded.")


    logging.debug("Clearing data...")
    brand_datatable.iloc[:, 0] = brand_datatable.iloc[:, 0].astype(str)
    brand_datatable.iloc[:, 1] = brand_datatable.iloc[:, 1].astype(str)
    brand_datatable.iloc[:, 2] = brand_datatable.iloc[:, 2].astype(str)
    brand_datatable.iloc[:, 3] = brand_datatable.iloc[:, 3].astype(str)
    raw_input_datatable.insert(1, 'Сумма', raw_input_datatable.iloc[:, 1:].sum(axis=1))
    raw_input_datatable.insert(0, 'Бренд', None)
    input_datatable = raw_input_datatable[raw_input_datatable['Сумма'] != 0]
    input_datatable.index = input_datatable.index + 2
    logging.info(f"Cleared input sheet:\n{input_datatable}")
    # result_datatable = pd.DataFrame({})
    logging.debug("Data've been cleared.")

    logging.debug("Analyzing data...")
    comparing_results = {}
    for brandDT_RowIndex in brand_datatable.index:
        brand_names = []
        if brand_datatable.iat[brandDT_RowIndex, 0] != "nan":
            brand_main_name = str(brand_datatable.iat[brandDT_RowIndex, 0])
            brand_names.append(brand_main_name)
        if brand_datatable.iat[brandDT_RowIndex, 1] != "nan":
            brand_second_name = brand_datatable.iat[brandDT_RowIndex, 1]
            brand_names.append(brand_second_name)
        if brand_datatable.iat[brandDT_RowIndex, 2] != "nan":
            brand_currupted_names = brand_datatable.iloc[brandDT_RowIndex, 2]
            brand_list_of_currupted_names = brand_currupted_names.split(",")
            brand_names.extend(brand_list_of_currupted_names)
        logging.debug(f"Brand names:{brand_names}")

        for inputDT_RowIndex in input_datatable.index:
            # logging.debug(inputDT_RowIndex)
            isMatched = None
            # matched_name = None
            input_brand_name = str(input_datatable.at[inputDT_RowIndex, 'Наименование']).lower().strip()
            
            for brand_name in brand_names:
                brand_name = str(brand_name).lower().strip()
                isMatched = f'{brand_name}' in f'{input_brand_name}'
                # isMatched = re.search(rf' {input_brand_name} ', fr' {brand_name} ')
                # if isMatched is None:
                #     isMatched = re.search(rf'\W{input_brand_name}\W', rf' \W{brand_name}\W ')
                if isMatched:
                    # matched_name = brand_main_name
                    logging.debug(f'Input brand:{inputDT_RowIndex}: {input_brand_name} - {brand_name}')
                    if input_datatable.at[inputDT_RowIndex, 'Бренд'] == None:
                        logging.debug(f"None appeared: {input_datatable.at[inputDT_RowIndex, 'Бренд']}")
                        input_datatable.at[inputDT_RowIndex, 'Бренд'] = [brand_main_name]
                    else:
                        logging.debug(f"Not None, there is: {input_datatable.at[inputDT_RowIndex, 'Бренд']}")
                        for matched_name in input_datatable.at[inputDT_RowIndex, 'Бренд']:
                            logging.debug(f"Comparing {matched_name} to {brand_main_name}")
                            if matched_name == brand_main_name:
                                logging.debug(f"Exists: {input_datatable.at[inputDT_RowIndex, 'Бренд']}")
                                break
                            else:
                                logging.debug(f"Doesn't exists: {input_datatable.at[inputDT_RowIndex, 'Бренд']}, adding: {brand_main_name}")
                                # input_datatable.at[inputDT_RowIndex, 'Бренд'] = 
                                input_datatable.at[inputDT_RowIndex, 'Бренд'].append(brand_main_name)
                                logging.debug(f"Result of adding: {input_datatable.at[inputDT_RowIndex, 'Бренд']}")

    logging.debug(f"Searching for several brands in:\n{input_datatable}")
    for brandDT_RowIndex in brand_datatable.index:
        brand_main_name = str(brand_datatable.iat[brandDT_RowIndex, 0])
        exception_brand_names = brand_datatable.iat[brandDT_RowIndex, 3]
        if exception_brand_names != None and exception_brand_names != 'nan':
            exception_brand_names_list = exception_brand_names.split(",")
            logging.debug(f"Exceptions rule, for brand: {brand_main_name}, found: {exception_brand_names}, that've been split in: {exception_brand_names_list}")
            for exception_brand_name in exception_brand_names_list:
                for inputDT_RowIndex in input_datatable.index:
                    logging.debug(f"Comparing exception: {exception_brand_name} to value in Row Index: {inputDT_RowIndex}, from Data Table:\n{input_datatable}")
                    several_brand_name_list = input_datatable.at[inputDT_RowIndex, "Бренд"]
                    changed_several_brand_name_list = []
                    several_brand_names_for_removal = []
                    logging.debug(several_brand_name_list)
                    if several_brand_name_list != None and len(several_brand_name_list) > 1 and isinstance(several_brand_name_list, list):
                        for one_of_the_brand_names_index in range(0, len(several_brand_name_list)):
                            one_of_the_brand_names = several_brand_name_list[one_of_the_brand_names_index]
                            if exception_brand_name == one_of_the_brand_names and one_of_the_brand_names != None:
                                several_brand_names_for_removal.append(brand_main_name)
                        if len(several_brand_names_for_removal) > 0:
                            for brand_name_for_removal in several_brand_names_for_removal:
                                try:
                                    logging.debug(f"Removing: {brand_name_for_removal} from: {several_brand_name_list}")
                                    several_brand_name_list.remove(brand_name_for_removal)
                                except: pass
                    logging.debug("Should we make str() out of list():"+f"{several_brand_name_list}")
                    if several_brand_name_list != None and isinstance(several_brand_name_list, list):
                        logging.debug("     Making str() out of list():"+f"{several_brand_name_list}")
                        input_datatable.at[inputDT_RowIndex, "Бренд"] = str(several_brand_name_list[0])
                        logging.debug(f"     Result of remaking:{input_datatable.at[inputDT_RowIndex, 'Бренд']}")
                        
        else:
            pass
    logging.debug(f"Result:\n {input_datatable}")
    
    logging.debug("Analysis done.")

    logging.debug("Saving Resultes...")
    logging.debug(f"Saving input datatable to {OUTPUT_DATA_FILENAME}")
    output_datatable = input_datatable
    output_full_datable = output_datatable
    output_full_datable.to_excel(OUTPUT_DATA_FILENAME, "Расшифровка ввода")
    logging.info(f"Grouped and summed data:\n{input_datatable}")
    output_aggregated_datatable = output_datatable[['Бренд', 'Сумма']].groupby('Бренд')['Сумма'].sum()
    logging.debug(f"Aggregated data:\n{output_aggregated_datatable}")
    
    with pd.ExcelWriter(OUTPUT_DATA_FILENAME, mode='a') as writer:
        output_aggregated_datatable.to_excel(writer, 'Вывод')

    logging.debug("Results are saved.")


if __name__ == '__main__':
    print("STARTING________________________________________")
    logging.debug("START________________________________________")
    main_algorith()
    logging.debug("FINISHED_______________________________________")
    print("FINISHED_______________________________________")
