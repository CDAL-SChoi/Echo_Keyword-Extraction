import numpy as np
import pandas as pd
import csv
import re


#삼성병원 데이터 처리
class EJ_format:
    def __init__(self):
        self.data = None
        self.path = "extract"
        self.units = ['mmhg', 'mm', '/m²', '%', 'cm/sec', 'msec', 'kg', 'g/㎡', 'g', 'cm', 'ms', 'm/s', 'ml/m2', '㎡']
        self.div = ['/', '~']
        self.delidx = ['M-MODE Study(mm)', '2D Echocardiography', 'LV Function', 'Global Function(%)', 'Doppler Study', 'Myocardial Strain Study']
        """
        self.default_EJ900 = ['Height', 'Weight', 'BSA', 'BP', 'M-MODE Study(mm)',
           'LVID(D/S)', 'Septum/LVPW', 'Aorta/LA', 'RVID(D/S)',
           'LV mass', 'LV mass index', 'RWT', 'RWT2', '2D Echocardiography',
           'Chamber', 'Valvular Structure', 'LV Function', 'Regional Wall Motion',
           'Global Function(%)', 'Qualification', 'Quantitation', 'RV Function',
           'Pericardium', 'Doppler Study', 'MV', 'E/A', 'DT', 'E\'/A\'', 'E/E\'',
           'AV', 'TV', 'PV', 'Estimated PA Systolic Pressure', 'Other Findings',
           'Myocardial Strain Study', 'LV GLPSS_LAX', 'LV GLPSS_A4C', 'LV GLPSS_A2C',
           'LV GLPSS_Avg', 'Conclusions']
        """
        self.default_EJ900 = ['Height', 'Weight', 'BSA', 'BP',
           'LVID(D/S)', 'Septum/LVPW', 'Aorta/LA', 'RVID(D/S)',
           'LV mass', 'LV mass index', 'RWT', 'RWT2',
           'Chamber', 'Valvular Structure', 'Regional Wall Motion',
           'Qualification', 'Quantitation', 'RV Function',
           'Pericardium', 'MV', 'Mean PG', 'PHT', 'PG(Peak/Mean)', 'E/A', 'DT', 'E\'/A\'', 'E/E\'',
           'AV', 'TV', 'PV', 'Estimated PA Systolic Pressure', 'Other Findings',
           'LV GLPSS_LAX', 'LV GLPSS_A4C', 'LV GLPSS_A2C', 'LV GLPSS_Avg','Conclusions']

        #self.New_format = None
        self.New_format = ['BP', 'Ht', 'Wt', 'BSA', 'LVIDd', 'LVIDs','IVSd', 'LVPWd','E', 'e`', 'A', 'a`',
                            'LA', 'LVEF', 'Ao', 'DT', 'LAVI', 'A-L', 'LVMI', 'RWT',
                            '1. LV', '2. RV', '3. Atrium', '4. Valve', '5. Great vessel', 'Abdominal aorta size(AP/T)',
                            '6. Pericardial effusion', '7. Mass, thrombi or vegetation', '8. RV systolic pressure by TR Vmax']

        self.dividx = [['BP', 'SBP', 'DBP'], ['LVID(D/S)','LVID(D)','LVID(S)'],
                        ['Septum/LVPW','Septum','LVPW'], ['Aorta/LA','Aorta','LA'],
                        ['RVID(D/S)','RVID(D)','RVID(S)'], ['Qualification','Qualification(min)','Qualification(max)'],
                        ['Quantitation', 'Quantitation(min)','Quantitation(max)'],['E/A','E','A'],
                        ['E\'/A\'','E\'','A\''], ['PG(Peak/Mean)', 'PG(Peak)', 'PG(Mean)']]

        self.numidx = ['Height', 'Weight', 'BSA', 'SBP', 'DBP', 'LVID(D)','LVID(S)',
                        'Septum','LVPW','Aorta','LA','RVID(D)','RVID(S)', 'LV mass',
                        'LV mass index', 'RWT', 'RWT2', 'Qualification(min)','Qualification(max)',
                        'Quantitation(min)','Quantitation(max)','E','A','DT', 'E\'','A\'','E/E\'',
                        'PG(Peak)', 'PG(Mean)', 'PHT', 'Mean PG', 'Estimated PA Systolic Pressure',
                        'LV GLPSS_LAX', 'LV GLPSS_A4C', 'LV GLPSS_A2C', 'LV GLPSS_Avg',
                        'Ht', 'Wt', 'LVIDd', 'LVIDs','IVSd', 'LVPWd','E', 'e`', 'A', 'a`',
                        'LA', 'LVEF', 'Ao', 'DT', 'LAVI', 'LVMI', 'RWT']

    def EJ900_format(self, format):
        if format is not None: 
            self.default_EJ900 = format
        
    def Define_New_format(self, format):
        if format is not None: 
            self.New_format = format
        
    def data_load(self, filename=None):
        if filename is None: 
            print("There is no input data")
            if self.data is not None:
                print("Using the previous input data")
        else:
            reader = csv.reader(open(filename, 'r', encoding='cp949'))
            lines=[]
            print("Loading...")
            for line in reader:
                lines.append(line)
            #self.data = np.array(lines, dtype='U')
            self.data = lines
            print("Complete")
        
    def Start(self, save=True, path=None, format=None, verbose=False):
        if self.data is None: print("There is no input data")
        else:
            if save:
                if path is not None: self.path = path
                self.MakeDB(self.data, format)
                    
    def my_split(self, text, delimiter):
        token = []
        for i in range(len(text)):
            tmp = text[i].split(delimiter)
            for j in range(len(tmp)):
                token.append(tmp[j].strip())
        return token
        
    def my_division(self, text, div):
        res = []
        spl = text
        boores = True
        for d in div:
            spl = self.my_split(spl, d)
        if len(spl) == 2:
            res.append(spl[0].strip())
            res.append(spl[1].strip())
            boores = False
        else:
            res.append('')
            res.append('')
            boores = False
        if boores: res = [text, '']
        return res

    def delunits(self, text, units):
        res = []
        for i in range(len(text)):
            a = text[i].lower()
            for unit in units:
                if unit in a:
                    a = a.replace(unit, '')
                    a = a.strip()
            a = re.sub(r'\([^)]*\)', '', a)
            a = re.sub(r'\([^)]*', '', a)
            a = re.sub(r'[^(]*\)', '', a)
            # 괄호 내용이 있는 경우 과감하게 버리기
            if self.is_number(a):
                res.append(a)
            else: res.append('')
        return res
        
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def date_time(self, text):
        regex = re.compile(r'(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d)')  # 2019-07-16 10:00 의 형식
        matchobj = regex.search(text)
        if matchobj != None:
            return [matchobj.group(1), matchobj.group(2)]
        else:
            return ['', '']
            
    def findnext(self, nparray, i):
        for k in range(i+1, min(i+8, len(nparray))):
            if nparray[k] == 1.0:
                return k
        return i+2

    def my_extract(self, text, format):
        dividx_ = []
        numidx_ = []
        content_ = ['Date', 'Time']
        content_.extend(format)
        for i in format:
            for j in self.dividx:
                if i is j[0]:
                    dividx_.append(format.index(i))  # divide index를 스스로 찾기
                    content_.insert(content_.index(i)+1, j[2])
                    content_.insert(content_.index(i) + 1, j[1])
                    content_.remove(i)

        for i in content_:        # number index 스스로 찾기
            for j in self.numidx:
                if i is j:
                    numidx_.append(content_.index(i))

        label = text[0][0:6]
        label.extend(content_)

        opening_1 = open(self.path + "_EJ900.csv", 'w', newline='', encoding='ms949')
        csvwriter_1 = csv.writer(opening_1)
        csvwriter_1.writerow(label)


        for k in range(len(text)):
            data = text[k][6] #aaaaa

            sample = []
            sample.extend(text[k][0:6])
            sample.extend(self.date_time(data))
            
            data = data.split('▶')
            data = self.my_split(data, '- ')
            data = self.my_split(data, ':')
            data = self.my_split(data, ';')
            
            #if (text[k][0] == "EJ900") or (text[k][0] == "EJ900D"): #aaaaa
            if True:
                for preprocessing in ['=', '&', '\n\n\n', '\n\n', '\n', '   ']:
                    data = self.my_split(data, preprocessing)
                for i in self.delidx:
                    if i in data:
                        data.remove(i)  # 후에 수정될 수 있음

                data_index = []
                data_binary = np.zeros(len(data))
                for i in format:
                    if i not in data:
                        data_index.append('')
                    else:
                        data_index.append(data.index(i))
                        data_binary[data.index(i)] = 1
                for i in range(len(data_index)):
                    if data_index[i] is not '':
                        k = len(sample)-6
                        a = data[(data_index[i]+1):(self.findnext(data_binary, data_index[i]))]
                        a = [e for e in a if e != '']
                        a = [('\n'.join(a)).strip()]
                        if i in dividx_:
                            a = self.my_division(a, self.div)
                        if k in numidx_:
                            a = self.delunits(a, self.units)
                        sample.extend(a)
                    else:
                        a = ['']
                        if i in dividx_:
                            a.append('')
                        sample.extend(a)
                #sample.append(('\n'.join(con_)).strip())
                csvwriter_1.writerow(sample)

                
            else:
                a=[]

            #스플릿 진행하여 conclusion 이후 부분을 먼저 빼내고, 그 후 나머지부분에 대해서 = split 진행
        opening_1.close()

    def MakeDB(self, data, format):
        if format == 'New':
            format = self.New_format
        else: format = self.default_EJ900
        self.my_extract(data, format)

    def saveDB(self):
        #self.FINALRES.to_csv(self.path, index=False, encoding='ms949')
        return 0