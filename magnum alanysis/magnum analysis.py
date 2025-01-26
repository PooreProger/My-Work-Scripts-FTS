import os
import logging
import pandas as pd
import re
from functools import reduce


PATH_TO_CURRENT_DIR = os.path.dirname(__file__)

LOGGING_FILENAME = "magnum an logz.log"
LOGGING_FILEPATH = PATH_TO_CURRENT_DIR+"\\"+LOGGING_FILENAME

logging.basicConfig(
    level=logging.DEBUG,
    filename=LOGGING_FILEPATH,
    encoding='utf-8',
    format='%(asctime)s %(levelname)s %(message)s'
)

BRAND_DATA_FILE = "Бренды.xlsx"
BRAND_DATA_SHEET = "Реестр Брендов для Расшифровки"
BRAND_DATA_FILE_PATH = PATH_TO_CURRENT_DIR+'\\'+BRAND_DATA_FILE
INCOME_DATA_FILE = "Входящая расшифровка.xlsx"
INCOME_DATA_SHEET = "Sheet1"
PATH_TO_INCOME_DATA = PATH_TO_CURRENT_DIR+"\\"+INCOME_DATA_FILE
INPUT_COLUMNS = {"Наименование услуги": 3, 
                  "Наименование товара": 15, 
                 "Сумма": 28,  
                 "Метод расчёта": 4,
                 "Период начало": 6,
                 "Период конце": 7,
                 "Номер договора": 5}
OUTPUT_DATA_FILENAME = "Вывод расшифровки Magnum.xlsx"
OUTPUT_DATA_FILEPATH = PATH_TO_CURRENT_DIR+"\\"+OUTPUT_DATA_FILENAME

logging.debug("Path:"+PATH_TO_CURRENT_DIR)
logging.debug("Path to file:"+PATH_TO_INCOME_DATA)


def brands_preparing(data_sheet):
    data_sheet.iloc[:, 0] = data_sheet.iloc[:, 0].astype(str)
    data_sheet.iloc[:, 1] = data_sheet.iloc[:, 1].astype(str)
    data_sheet.iloc[:, 2] = data_sheet.iloc[:, 2].astype(str)
    data_sheet.iloc[:, 3] = data_sheet.iloc[:, 3].astype(str)
    data_sheet.iloc[:, 4] = data_sheet.iloc[:, 4].astype(str)
    all_brands = data_sheet.iloc[:, :4].agg(", ".join, axis=1)
    data_sheet.insert(1, "Бренды", all_brands)
    data_sheet = data_sheet.iloc[:, [0, 1, 4, 5]]
    return data_sheet

def brand_definder(raw_data_str, brands_sheet):
    # logging.debug(f"Defining: {raw_data_str}")
    found_brand_names = []
    data_str = str(raw_data_str).lower().strip().replace(" ", " ")
    for brandDS_RowIndex in brands_sheet.index:
        brand_main_name = brands_sheet.iat[brandDS_RowIndex, 0]
        brand_names_list = str(brands_sheet.iat[brandDS_RowIndex, 1]).split(", ")
        brand_names_exceptions_list = str(brands_sheet.iat[brandDS_RowIndex, 2]).split(", ")
        isException = None
        isMatch = None


        if brands_sheet.iat[brandDS_RowIndex, 0] == "nan": pass
        else:
            # isException
            for exception_word in brand_names_exceptions_list:
                exception_word = str(exception_word).lower().strip()
                if exception_word != "nan":
                    isException = re.search(fr'.{exception_word}.', fr'.{data_str}.')
                    if isException:
                        break
                else: pass
            
            # isMatch
            if isException is None:
                # logging.debug(f"    Going for list: {brand_names_list}")
                for brand_name in brand_names_list:
                    # logging.debug(brand_name)
                    brand_name = str(brand_name).lower().strip()
                    # logging.debug(f"        {brand_name}")
                    if brand_name != "nan":
                        # logging.debug(f"          Looking: {brand_name} in: {data_str}")
                        isMatch = re.search(fr'.{brand_name}.', fr'.{data_str}.')
                        if isMatch: 
                            break
            else: pass
        
        if isMatch:
            found_brand_names.append(brand_main_name)
    

    if len(found_brand_names) > 0:
        for brandDS_RowIndex in brands_sheet.index:
            brand_main_name = str(brands_sheet.iat[brandDS_RowIndex, 0])
            contr_brand_names = str(brands_sheet.iat[brandDS_RowIndex, 3]).split(", ")
            for contr_brand in contr_brand_names:
                if contr_brand != "None" and contr_brand != "nan":
                    for found_brand in found_brand_names:
                        if contr_brand == found_brand:
                            # logging.debug(f"Brand: {found_brand} - contrs with: {contr_brand}, so revoming {brand_main_name}")
                            try: 
                                found_brand_names.remove(brand_main_name)
                            except: pass

    logging.debug(f"In: {data_str} | Found: {found_brand_names}")
    if len(found_brand_names) > 0:
        return str(", ".join(found_brand_names))
    else: return ""


def magnum_analysis_algorithm(path_to_input_file, input_sheet_name, output_filepath):
    raw_input_datatable = pd.read_excel(path_to_input_file, input_sheet_name)
    logging.debug(f"Raw data: \n{raw_input_datatable}")
    input_datatable = raw_input_datatable.iloc[16:, list(INPUT_COLUMNS.values())]
    input_datatable.columns = list(INPUT_COLUMNS.keys())
    input_datatable.insert(1, 'Бренд', None)
    input_datatable.reset_index(drop=True, inplace=True)
    logging.debug(f"Data: \n{input_datatable}")

    brand_datatable = pd.read_excel(BRAND_DATA_FILE_PATH, BRAND_DATA_SHEET)
    brand_datatable = brands_preparing(brand_datatable)


    for inputDT_RowIndex in input_datatable.index:
        item_name = input_datatable.iat[inputDT_RowIndex, 2]
        definded_brand = brand_definder(item_name, brand_datatable)
        input_datatable.at[inputDT_RowIndex, 'Бренд'] = definded_brand
    logging.debug(f"Data with brands:\n{input_datatable}")

    list_of_sum_col = list(input_datatable.columns[[-1, 1]])
    brand_sum = input_datatable.groupby(list_of_sum_col, as_index=False)[input_datatable.columns[3]].sum()
    logging.debug(f"Summed brands:\n{brand_sum}")

    doc_sum = input_datatable.iloc[:, [-1, 3]].groupby(input_datatable.columns[-1], as_index=False)[input_datatable.columns[3]].sum()
    doc_sum.rename(columns={"Сумма":"Общая сумма"}, inplace=True)

    logging.debug(f"Sum doc:\n{doc_sum}")

    date_min = input_datatable.groupby(list_of_sum_col, as_index=False)[input_datatable.columns[5]].min()
    # logging.debug(date_min)
    date_max = input_datatable.groupby(list_of_sum_col, as_index=False)[input_datatable.columns[6]].max()
    # logging.debug(date_max)
    merged_dates = pd.merge(date_min, date_max, how='inner', on=list_of_sum_col)
    logging.debug(merged_dates)
    
    merged_SumNDate = pd.merge(brand_sum, merged_dates, how='inner', on=list_of_sum_col)
    logging.debug(merged_SumNDate)
    merged_datatable = pd.merge(merged_SumNDate, doc_sum, how='outer', on=list_of_sum_col[0])
    logging.debug(f"\n{merged_datatable}")
    presorted_datatable = merged_datatable.iloc[:, [5, 1, 2, 3, 4, 0]].sort_values(["Номер договора", "Бренд"])
    logging.debug(f"THE END\n{presorted_datatable}")

    presorted_datatable.to_excel(output_filepath)
    # with pd.ExcelWriter(OUTPUT_DATA_FILENAME, mode='a') as writer:
    #     presorted_datatable.to_excel(writer, "Расшифровка")









if __name__ == '__main__':
    magnum_analysis_algorithm(PATH_TO_INCOME_DATA, INCOME_DATA_SHEET, OUTPUT_DATA_FILEPATH)
