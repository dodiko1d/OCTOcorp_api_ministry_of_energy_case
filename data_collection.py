import openpyxl


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


