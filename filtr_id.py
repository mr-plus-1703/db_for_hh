import pandas as pd

# Пути к файлам где есть одинаковые id
file_paths = [
    'df_hh_ru_privod.xlsx',
    'df_hh_ru_АСУ ТП.xlsx',
    'df_hh_ru_Снабжение.xlsx'
]

# Чтение файлов и объединение их в один DataFrame
dfs = [pd.read_excel(file) for file in file_paths]
combined_df = pd.concat(dfs, ignore_index=True)

# Удаление дубликатов по колонке 'id'
unique_df = combined_df.drop_duplicates(subset='id', keep='first')

# Сохранение результата в новый Excel файл
output_path = 'filtr_for_id_all.xlsx'
unique_df.to_excel(output_path, index=False)
