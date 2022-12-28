# import csv
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter
# from openpyxl.styles import Font, Border, Side
#
#
# class Vacancy:
#     currency_to_rub = {
#         "AZN": 35.68, "GEL": 21.74, "RUR": 1, "BYR": 23.91, "EUR": 59.90, "KGS": 0.76, "KZT": 0.13, "USD": 60.66, "UZS": 0.0055,"UAH": 1.64,
#     }
#
#     def __init__(self, vacancy):
#         self.salary_to = int(float(vacancy['salary_to']))
#         self.salary_from = int(float(vacancy['salary_from']))
#         self.salary_currency = vacancy['salary_currency']
#         self.name = vacancy['name']
#         self.year = int(vacancy['published_at'][:4])
#         self.salary_average = self.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2
#         self.area_name = vacancy['area_name']
#
# class Input:
#     def __init__(self):
#         self.f_name = input('Введите название файла: ')
#         self.vac_name = input('Введите название профессии: ')
#
#         data = DataSet(self.f_name, self.vac_name)
#         stat, stat_seconds, stat_thirds, stat_fourth, stat_fifth, stat_six = data.stat()
#         data.prints(stat, stat_seconds, stat_thirds, stat_fourth, stat_fifth, stat_six)
#
#         rep = Report(self.vac_name, stat, stat_seconds, stat_thirds, stat_fourth, stat_fifth, stat_six)
#         rep.exel_outs()
#
# class DataSet:
#     def __init__(self, f_name, vac_name):
#         self.file_name = f_name
#         self.vacancy_name = vac_name
#
#     @staticmethod
#     def crems(dic, k, amount):
#         if k in dic:
#             dic[k] += amount
#         else:
#             dic[k] = amount
#
#     @staticmethod
#     def avr(dic):
#         dic_new = {}
#         for k, v in dic.items():
#             dic_new[k] = int(sum(v) / len(v))
#         return dic_new
#
#     def read_csv(self):
#         with open(self.file_name, mode='r', encoding='utf-8-sig') as f:
#             read = csv.reader(f)
#             head = next(read)
#             len_head = len(head)
#             for line in read:
#                 if '' not in line and len(line) == len_head:
#                     yield dict(zip(head, line))
#
#     def stat(self):
#         sal = {}
#         vac_name_sal = {}
#         city = {}
#         count = 0
#
#         for dict_vac in self.read_csv():
#             vac = Vacancy(dict_vac)
#             self.crems(sal, vac.year, [vac.salary_average])
#             if vac.name.find(self.vacancy_name) != -1:
#                 self.crems(vac_name_sal, vac.year, [vac.salary_average])
#             self.crems(city, vac.area_name, [vac.salary_average])
#             count += 1
#
#         nums = dict([(key, len(value)) for key, value in sal.items()])
#         nums_names = dict([(key, len(value)) for key, value in vac_name_sal.items()])
#
#         if not vac_name_sal:
#             vac_name_sal = dict([(key, [0]) for key, value in sal.items()])
#             nums_names = dict([(key, 0) for key, value in nums.items()])
#
#         stat = self.avr(sal)
#         stat_seconds = self.avr(vac_name_sal)
#         stat_thirds = self.avr(city)
#
#         stat_fourth = {}
#         for year, sal in city.items():
#             stat_fourth[year] = round(len(sal) / count, 4)
#         stat_fourth = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in stat_fourth.items()]))
#         stat_fourth.sort(key=lambda a: a[-1], reverse=True)
#         stat_fifth = stat_fourth.copy()
#         stat_fourth = dict(stat_fourth)
#         stat_thirds = list(filter(lambda x: x[0] in list(stat_fourth.keys()), [(k, v) for k, v in stat_thirds.items()]))
#         stat_thirds.sort(key=lambda x: x[-1], reverse=True)
#         stat_thirds = dict(stat_thirds[:10])
#         stat_fifth = dict(stat_fifth[:10])
#
#         return stat, nums, stat_seconds, nums_names, stat_thirds, stat_fifth
#
#     @staticmethod
#     def prints(stat, stat_seconds, stat_thirds, stat_fourth, stat_fifth, stat_six):
#         print('Динамика уровня зарплат по годам: {0}'.format(stat))
#         print('Динамика количества вакансий по годам: {0}'.format(stat_seconds))
#         print('Динамика уровня зарплат по годам для выбранной профессии: {0}'.format(stat_thirds))
#         print('Динамика количества вакансий по годам для выбранной профессии: {0}'.format(stat_fourth))
#         print('Уровень зарплат по городам (в порядке убывания): {0}'.format(stat_fifth))
#         print('Доля вакансий по городам (в порядке убывания): {0}'.format(stat_six))
#
#
#
# class Report:
#     def __init__(self, n_vac, stat, stat_seconds, stat_thirds, stat_fourt, stat_fifth, stat_six):
#         self.wordbook = Workbook()
#         self.n_vac = n_vac
#         self.stat = stat
#         self.stat_seconds = stat_seconds
#         self.stat_thirds = stat_thirds
#         self.stat_fourt = stat_fourt
#         self.stat_fifth = stat_fifth
#         self.stat_six = stat_six
#
#     def exel_outs(self):
#         w = self.wordbook.active
#         w.title = 'Статистика по годам'
#         w.append(['Год', 'Средняя зарплата', 'Средняя зарплата - ' + self.n_vac, 'Количество вакансий', 'Количество вакансий - ' + self.n_vac])
#         for y in self.stat.keys():
#             w.append([y, self.stat[y], self.stat_thirds[y], self.stat_seconds[y], self.stat_fourt[y]])
#
#         data = [['Год ', 'Средняя зарплата ', ' Средняя зарплата - ' + self.n_vac, ' Количество вакансий', ' Количество вакансий - ' + self.n_vac]]
#         wid_column = []
#         for line in data:
#             for x, c in enumerate(line):
#                 if len(wid_column) > x:
#                     if len(c) > wid_column[x]:
#                         wid_column[x] = len(c)
#                 else:
#                     wid_column += [len(c)]
#
#         for x, column_width in enumerate(wid_column, 1):  # ,1 to start at 1
#             w.column_dimensions[get_column_letter(x)].width = column_width + 2
#
#         data = []
#         data.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий'])
#         for (city_f, v_f), (city_s, v_s) in zip(self.stat_fifth.items(), self.stat_six.items()):
#             data.append([city_f, v_f, '', city_s, v_s])
#         w_s = self.wordbook.create_sheet('Статистика по городам')
#         for line in data:
#             w_s.append(line)
#
#         wid_column = []
#         for line in data:
#             for x, c in enumerate(line):
#                 c = str(c)
#                 if len(wid_column) > x:
#                     if len(c) > wid_column[x]:
#                         wid_column[x] = len(c)
#                 else:
#                     wid_column += [len(c)]
#
#         for x, column_width in enumerate(wid_column, 1):  # ,1 to start at 1
#             w_s.column_dimensions[get_column_letter(x)].width = column_width + 2
#
#         bold = Font(bold=True)
#         for c in 'ABCDE':
#             w[c + '1'].font = bold
#             w_s[c + '1'].font = bold
#
#         for i, _ in enumerate(self.stat_fifth):
#             w_s['E' + str(i + 2)].number_format = '0.00%'
#
#         thin = Side(border_style='thin', color='00000000')
#
#         for line in range(len(data)):
#             for c in 'ABDE':
#                 w_s[c + str(line + 1)].border = Border(left=thin, bottom=thin, right=thin, top=thin)
#
#         self.stat[1] = 1
#         for line, _ in enumerate(self.stat):
#             for c in 'ABCDE':
#                 w[c + str(line + 1)].border = Border(left=thin, bottom=thin, right=thin, top=thin)
#
#         self.wordbook.save('report.xlsx')

#if __name__ == '__main__':
#     Input()




























def get_city(city):
    print(city)

if __name__ == '__main__':
    get_city('Praha')



































