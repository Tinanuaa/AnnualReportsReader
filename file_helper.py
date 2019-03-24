from os import path
from config_helper import config
import zipfile
import unicodecsv as csv
from datetime import datetime
import os
import pandas as pd
from dateutil.relativedelta import relativedelta

def save_pdf(content,filename,folder):
    full_folder_path = check_folder(folder)
    output_name = path.join(full_folder_path, filename + '.pdf')
    with open(output_name, 'wb') as pdf:
        pdf.write( content)

    return output_name

def check_folder(output_folder):
    if not os.path.exists(config["output_folder"]):
        os.makedirs(config["output_folder"])
    if isinstance(output_folder, list):
        folder = config["output_folder"]
        for sub_folder in output_folder:
            folder = os.path.join(folder, sub_folder)
            if not os.path.exists(folder):
                os.makedirs(folder)
        output_folder = folder

    else:
        if output_folder != config["output_folder"]:
            folder = os.path.join(config["output_folder"], output_folder)
            if not os.path.exists(folder):
                os.makedirs(folder)
            output_folder = folder

    return output_folder


def write_to_excel(filename, df, column=None, name="Report", date_in_filename=datetime.now(),
                   output_folder=config["output_folder"]):
    output_folder = check_folder(output_folder)

    file = os.path.join(output_folder, filename + "_" + date_in_filename.strftime("%Y-%m-%d") + ".xlsx")

    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    if column is None:
        df.to_excel(writer, index=False, encoding='utf-8', sheet_name=name)
    else:
        df.to_excel(writer, columns=column, index=False, encoding='utf-8', sheet_name=name)
    writer.save()
    writer.close()

    return file


def write_multiple_df_to_excel(file, data, mode="MULTIPLESHEET", date_in_filename=datetime.now(),
                               output_folder=config["output_folder"]):
    output_folder = check_folder(output_folder)

    file = os.path.join(output_folder, file + date_in_filename.strftime("%Y-%m-%d") + ".xlsx")
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    if mode == "MULTIPLESHEET":
        for sheet, row in data.items():
            row["data"].to_excel(writer, columns=row["column"], index=False, encoding='utf-8', sheet_name=sheet)
    else:
        for sheet, data_list in data.items():
            for index, row in enumerate(data_list):
                row["data"].to_excel(writer, columns=row["column"], index=False, encoding='utf-8', sheet_name=sheet,
                                     startrow=row["startrow"], startcol=row["startcol"])

    writer.save()
    writer.close()

    return file


def zip_files(files, filename, folder=config["output_folder"], folder_date=datetime.now() - relativedelta(months=1)):
    if folder == config["output_folder"]:
        loczip = os.path.join(folder, filename)
    else:
        share_folder = os.path.join(folder, folder_date.strftime("%Y-%m"))
        if not os.path.exists(share_folder):
            os.makedirs(share_folder)

        loczip = os.path.join(share_folder, filename)

    with zipfile.ZipFile(loczip, "w", zipfile.ZIP_DEFLATED) as zip:
        for locfile in files:
            zip.write(locfile, os.path.basename(locfile))

    return loczip


def write_to_csv(entries, name="source", headers=None, folder="./output", name_date=True, date=datetime.today()):
    folder = os.path.join(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if name_date:
        filename = folder + "/" + name + "_" + date.strftime("%Y-%m-%d") + ".csv"
    else:
        filename = folder + "/" + name + ".csv"

    mode = "wb"
    if len(entries) > 0:
        dict = entries[0]
    else:
        return None

    if headers == None:
        for index, row in enumerate(entries):
            dict.update(entries[index])
        headers = dict.keys()

    with open(filename, mode) as f:
        # f.write(u'\ufeff'.encode('utf-8'))
        writer = csv.DictWriter(f, headers, encoding='utf-8')
        if mode != "ab" and mode != "a":
            writer.writeheader()
        writer.writerows(entries)
        return filename

