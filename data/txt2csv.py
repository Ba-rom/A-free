# 실행 : $pytho txt2csv.py (txt파일명) {(라벨숫자) (시작행) (마지막행)} {반복2} {반복3}
import sys
import pandas as pd

args = sys.argv[1:]
# print(args)
if (len(args) - 1) % 3 != 0:
    print('input error')
    sys.exit()

class_num = (len(args) - 1) // 3
# print(class_num)

data_path = 'C:\\Users\\ROM\\Project\\A-free\\data\\'

txt_file_name = data_path + 'txt_data\\' + args[0] + '.txt'
# print(txt_file_name)

# txt파일 Dataframe으로 읽어오기
df = pd.read_csv(txt_file_name, sep = ' ', header=None)
# print(df)

df['72'] = 0
for i in range(class_num):
    class_label = int(args[i*3+1])
    start_point = int(args[i*3+2])
    end_point = int(args[i*3+3])
    for j in range(start_point-1, end_point):
        df.iloc[j, df.columns.get_loc('72')] = class_label
# print(df)

# Dataframe을 csv 파일로 저장
csv_file_name = data_path + 'csv_data\\' + args[0] + '.csv'
df.to_csv(csv_file_name, index=False, header=False, float_format='%.2f')