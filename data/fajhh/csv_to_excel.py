import pandas as pd


def csv_to_xlsx_pd():
    csv = pd.read_csv('scheme.csv', encoding='utf-8')
    csv.to_excel('data.xlsx', sheet_name='培养方案信息')


if __name__ == '__main__':
    csv_to_xlsx_pd()
