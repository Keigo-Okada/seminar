library(tidyverse)
library(dplyr)

#複数のcsvファイルの読み込み
df_path <- list.files(path = "/Users/keigookada/Library/CloudStorage/OneDrive-KansaiUniversity/ゼミ/R4 ゼミデータ/一時保存_岡田/sample/" , full.names = T)
df <- do.call(rbind, lapply(df_path, function(x) read.csv(x, header=TRUE, stringsAsFactors = FALSE)))

#個別のcsvの場合
df = read.csv("/Users/keigookada/Desktop/Gian_Table.csv")

#agenda=”議案”
#付託の総数
futaku_ari <- df%>% filter(df$futaku == 1)
#議案総数
agenda <- df %>% filter(df$id_type == "1")
#委員会付託あり議案
agenda_futaku <- df %>% filter(df$id_type == "1",
                        df$futaku == 1)
#議案以外の付託あり案件
other <- df %>% filter(df$id_type != "1",
                       df$futaku == 1)
#可決された議案
adoption <- agenda %>% filter(agenda$result == "原案可決",
                              agenda$result=="可決")
#否決された議案
N_adoption <- agenda %>% filter(result != "原案可決",
                                result != "可決")

#nashi <- df %>% filter(df$付託 == 0)
#それぞれの数のカウント
futaku_ari <- nrow(futaku_ari)
agenda_futaku <- nrow(agenda_futaku)
agenda <- nrow(agenda)
other <- nrow(other)


#nashi <- nrow(nashi)
total <- nrow(df)

#全議案に対しての付託率
reference_per <- futaku_ari / total * 100
#議案種別が”議”の議案に対しての付託率
reference_agenda_per <- agenda_futaku / agenda * 100

write.csv(x = reference_per,
          file = "/Users/keigookada/Desktop/福知山市結果.csv")

