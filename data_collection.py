import openpyxl
import pandas as pd


class Data:
    def get_gdp(self, region_name: str, year: str):
        sheet = self.xlxs_opener('vrp_region.xlsx')
        year_value = {
            '2010': 'B',
            '2011': 'C',
            '2012': 'D',
            '2013': 'E',
            '2014': 'F',
            '2015': 'G',
            '2016': 'H',
            '2017': 'I',
            '2018': 'J'
        }
        # collection of data on gross domestic product per capita
        regions_list = {}
        try:
            for cell in range(5, 102):
                regions_list[sheet['A' + str(cell)].value] = \
                    sheet[year_value[year] + str(cell)].value
        except KeyError:
            "There's no such year"
        return regions_list[region_name]

    def get_resourses_per_capita(self, year: str):
        sheet = self.xlxs_opener('resourses_per_capita.xlsx')
        data_list = {}
        cell_number = {'2017': 'E', '2018': 'F'}

        for cell in range(7, 16):
            data_list[sheet['A' + str(cell)].value] = sheet[cell_number[year] + str(cell)].value

        return data_list

    def xlxs_opener(self, file_name):
        wb = openpyxl.reader.excel.load_workbook(filename=file_name)
        wb.active = 0
        data_sheet = wb.active
        return data_sheet

    def get_power_consumption(self):

        raw_df = pd.read_csv('consumption_data.csv',
                             sep=';',
                             header=0,
                             usecols=['M_DATE', 'E_USE_FACT', 'E_USE_PLAN'],
                             infer_datetime_format=True,
                             )

        # In original dataset intervals between measurements are kept in separate column
        # but specific time of each measurement isn't specified.
        # Therefore it's necessary to construct datetime column manually.
        raw_df['M_DATE'] = pd.to_datetime(raw_df['M_DATE']) \
                           + pd.to_timedelta(raw_df.index % 24, unit='H')
        return raw_df

    def get_urbanization(self):
        f = pd.read_csv('urbanization.csv',
                        sep=',',
                        header=0,
                        usecols=['YEAR', 'REGION', 'INDICATOR'],
                        infer_datetime_format=True)
        f['YEAR'] = pd.DataFrame(f['YEAR'])

        return f



