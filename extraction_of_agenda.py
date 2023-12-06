# -*- coding: utf-8 -*-

import re
import pandas as pd
import os
import json
import sys

#空のデータフレームと配列を作成
df = pd.DataFrame(columns=['base','type_gian','noise','name_gian','end_word','year','jiscode','file_name'])
result = []

#フォルダー指定の方法(フォルダー→フォルダー→textファイルの順に指定)
current_folder = "/Users/keigookada/Downloads/光市/"  # 現在のフォルダのパス
#フォルダー直下のフォルダー達を取得
sub_folders = [f.path for f in os.scandir(current_folder) if f.is_dir()]

#jsonファイルの読み込み
with open("/Users/keigookada/Desktop/seminar/code/agenda_py/gian.json", 'r',encoding='utf-8') as json_file:
  pattern = json.load(json_file)

#全角数字を全て半角数字に変換する自作関数
def convert_fullwidth_to_halfwidth(text):
  return re.sub(r'[０-９]', lambda x: chr(ord(x.group()) - 0xFEE0), text)

#サブフォルダの中の.txtファイルを読み込む
for sub_folder in sub_folders:
    for root, dirs, files in os.walk(sub_folder):
        for file in files:
          if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            #print(file)
          #エラーチェック
          textname = file[:file.find(".")] #str型
          ck = len(textname)
          if not ck == 13:
            print(file ,'はファイル名の記載に誤りがあります。')
            sys.exit()
                
          #テキストファイルをstr型で取得
          f = open(file_path, "r",encoding = "utf-8")
          text = f.read()
          print(file,'を実行中')
          f.close
          #市町村コードと年をファイル名から取得
          year = int(file[:4])
          jiscode = str(file[8:13])
          #使用する市の選択
          selected_pattern = pattern.get(jiscode)
          #print(text)
          tex = convert_fullwidth_to_halfwidth(text)

          #空白の削除
          tex = tex.replace("\u3000", "")
          tex = tex.replace("\n","")
          #print(tex)
          #正規表現とのマッチング
          matches = re.findall(selected_pattern, tex)
          for inner_list in matches:
              new_inner_list = tuple(inner_list) + (year,jiscode,file,)
              result.append(new_inner_list)

          #print(new_data)
          #print(len(new_data))
          #print(type(new_data))

          for row in result:
            df = df._append(pd.Series(row, index=df.columns), ignore_index=True)

          #df = df.append(pd.DataFrame(matches)) ##バージョンによって実行できない
          #print(df)

#ddf = df[df['base'].str.contains(pattern)]

specified_word = '号'
df['num_gian'] = df['base'].str.extract(f'(.+?{specified_word})')
df['name_gian'] = df['name_gian'].str.cat(df['end_word'], sep=' ')
df['name_gian'] = df['name_gian'].str.replace(' ', '')
df = df.drop(["base","noise","end_word"], axis=1) 
df_removed = df.drop_duplicates(subset=['num_gian', 'year'], keep='first')


df_removed = df_removed.reset_index(drop=True)
#print(df_removed)
df_removed.to_csv("/Users/keigookada/Desktop/光市.csv",encoding="cp932") #.csvの形式で絶対パスを使用