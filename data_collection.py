import openpyxl
import re


class Data:
    def get_gdp(self, region_name: str, year: str):

        wb = openpyxl.reader.excel.load_workbook(filename='vrp_region.xlsx')
        wb.active = 0
        data_sheet = wb.active

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
                regions_list[data_sheet['A' + str(cell)].value] = \
                    data_sheet[year_value[year] + str(cell)].value
        except KeyError:
            "There's no such year"
        return regions_list[region_name]

    def get_resourses_per_capita(self, year: str):

        file = openpyxl.reader.excel.load_workbook(filename='resourses_per_capita.xlsx')

        file.active = 0
        sheet = file.active
        data_list = {}

        cell_number = {'2017': 'E', '2018': 'F'}

        for cell in range(7, 16):
            data_list[sheet['A' + str(cell)].value] = sheet[cell_number[year] + str(cell)].value

        return data_list

    def get_power_consumption(self):

        with open('power_consumption.csv', 'r', encoding='utf-8') as f:
            file = f.readlines()

        indicators = []
        for line in file:
            s = line.split()[-1]
            lst = s.replace(';', ' ').split()
            indicators.append(lst[-1])

        new_list = list(map(lambda x: float(re.sub('\W+', '', x)), indicators[1:]))
        final_list = []
        for element in new_list:
            if element != 0:
                final_list.append(element)
            else:
                pass
        return final_list


