
import pandas as pd

import json
import os

# defining functions

def load_json_files(math_directory):
    json_data = {}
    for root, dirs, files in os.walk(math_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    json_data[file_path] = data
    return json_data

def remove_special_chars(df):
    def remove_chars(value):
        if isinstance(value, str):
            return ''.join(char for char in value if char not in ['<', '>', '%', '-'])
        else:
            return value
    for col in df.columns:
        df[col] = df[col].apply(remove_chars)
    return df

# loading math dataset

math_directory = '/Users/davidfrost/Documents/chatbot_math/chatbot_program/data/math/train'
json_data = load_json_files(math_directory)

# Convert the dictionary into a DataFrame
df_math = pd.DataFrame.from_dict(json_data, orient='index')
df_math.info()
# Reset index to have a column for filenames
df_math.reset_index(inplace=True)
df_math.rename(columns={'index': 'filename'}, inplace=True)
df_math = df_math.drop('filename', axis=1)
df_math = df_math.query("level != 'Level ?'")

# loading cse dataset
cse_path_file = "/Users/davidfrost/Documents/chatbot_math/chatbot_program/data/cse_dataset.xlsx"
df_or = pd.read_excel(cse_path_file)
df = df_or.copy()
df = remove_special_chars(df)
df.isnull().sum()
df.info()

selected_features = ['Geslacht', 'Faculteit', 'SOOnderwijsvorm', 'SOStudiejaartekst', 'UrenWisk_REC', '%Wisk_REC', '%fysica', 
'%chemie', '%biologie', 'Inspanning_frequentie', 'Inspanning_intensiteit', 'OudersdiplomaHO', 'Klassenraad_REC', 
'Zomercursus_New', 'Motivatie_Doorzettingsvermogen_NORM', 'Time_Management_NORM', 'Concentratie_NORM', 
'Faalangst_NORM', 'Teststrategieen_NORM', 'Effort', 'Pressure Pref_REC', '% januari', 'CSE_januari', 
'% Juni', 'CSE_RECODED', '% September', 'Status student september']

additional_features = [f'y_{i}' for i in range(1, 1000)]

# Concatenate selected_features with additional_features
selected_columns = selected_features
# Select the subset of columns from the DataFrame
selected_df = df[selected_columns]

variables_list = selected_df.columns.tolist()

# Dictionary to store value_counts() for each variable
value_counts_dict = {}

# Iterate through each variable and calculate value_counts()
for variable in variables_list:
    value_counts_dict[variable] = selected_df[variable].value_counts()

# Print or use the value_counts() for each variable
for variable, value_counts in value_counts_dict.items():
    print(f"Value counts for variable '{variable}':")
    print(value_counts)
    print()  # Add an empty line for better readability

missing_values = selected_df.isnull().sum()

# Removing variables with higher missing values

var_to_drop = ['%biologie','Inspanning_intensiteit','Effort','% januari','% Juni','% September']
df_complete1 = selected_df.drop(columns=var_to_drop)
df_complete = df_complete1.dropna()

def con_geslacht(level):
  if level == "M":
    return 1
  else:
    return 0
  
def con_facu(value):
  if value == "FIRW":
    return 1
  else:
    return 0

def con_onderwijsvorm(value):
  if value == "ASO":
    return 1
  else:
    return 0

def con_studiejaartekst(value):
  if value == "WETENSCHAPPENWISKUNDE":
    return 1
  else:
    return 0
  
def con_urenwisk(level):
  if level == "8u":
    return 1
  elif level == "67u":
    return 2
  else:
    return 3

def con_wisk_rec(level):
  if level == "80":
    return 1
  elif level == "7080":
    return 2
  else:
    return 3

def con_fysica_rec(level):
  if level == "90":
    return 1
  elif level == "8090":
    return 2
  elif level == "7080":
    return 3
  elif level == "6070":
    return 4
  elif level == "60":
    return 4
  else:
    return 5

def con_chemi_rec(level):
  if level == "90":
    return 1
  elif level == "8090":
    return 2
  elif level == "7080":
    return 3
  elif level == "6070":
    return 4
  elif level == "60":
    return 4
  else:
    return 5
  
def con_inspanning(level):
  if level == "Helemaal niet hard":
    return 1
  elif level == "Niet hard":
    return 2
  elif level == "Noch hard noch niet hard":
    return 3
  elif level == "Hard":
    return 4
  else:
    return 5

def con_zomer(value):
  if value == "Ja":
    return 1
  else:
    return 0
  
def con_motivatie(level):
  if level == "Zeer zwak":
    return 1
  elif level == "Zwak":
    return 2
  elif level == "Gemiddeld":
    return 3
  elif level == "Goed":
    return 4
  else:
    return 5
def con_time(level):
  if level == "Zeer zwak":
    return 1
  elif level == "Zwak":
    return 2
  elif level == "Gemiddeld":
    return 3
  elif level == "Goed":
    return 4
  else:
    return 5
def con_concentratie(level):
  if level == "Zeer zwak":
    return 1
  elif level == "Zwak":
    return 2
  elif level == "Gemiddeld":
    return 3
  elif level == "Goed":
    return 4
  else:
    return 5

def con_faalangst(level):
  if level == "Zeer lage mate faalangst":
    return 1
  elif level == "Lage mate faalangst":
    return 2
  elif level == "Gemiddelde mate faalangst":
    return 3
  elif level == "Hoge mate faalangst":
    return 4
  else:
    return 5
def con_teststrategieen(level):
  if level == "Zeer zwak":
    return 1
  elif level == "Zwak":
    return 2
  elif level == "Gemiddeld":
    return 3
  elif level == "Goed":
    return 4
  else:
    return 5

def con_pressure(level):
  if level == "Laag":
    return 1
  elif level == "Gemiddeld":
    return 2
  else:
    return 3
def con_cse(level):
  if level == "30 CSE of dropout":
    return 1
  elif level == "3050 CSE":
    return 2
  elif level == "5080 CSE":
    return 3
  else:
    return 4

df_complete['sex'] = df_complete['Geslacht'].apply(con_geslacht)
df_complete['facu'] = df_complete['Faculteit'].apply(con_facu)
df_complete['sec_edu'] = df_complete['SOOnderwijsvorm'].apply(con_onderwijsvorm)
df_complete['math_edu'] = df_complete['SOStudiejaartekst'].apply(con_studiejaartekst)
df_complete['math_hours'] = df_complete['UrenWisk_REC'].apply(con_urenwisk)
df_complete['math_grade'] = df_complete['%Wisk_REC'].apply(con_wisk_rec)
df_complete['physics_grade'] = df_complete['%fysica'].apply(con_fysica_rec)
df_complete['chemi_grade'] = df_complete['%chemie'].apply(con_chemi_rec)
df_complete['effort'] = df_complete['Inspanning_frequentie'].apply(con_inspanning)
# df_complete['advising'] = df_complete['Klassenraad_REC'] #excluding
df_complete['summer_course'] = df_complete['Zomercursus_New'].apply(con_zomer)
df_complete['motivation'] = df_complete['Motivatie_Doorzettingsvermogen_NORM'].apply(con_motivatie)
df_complete['time_management'] = df_complete['Time_Management_NORM'].apply(con_time)
df_complete['concentration'] = df_complete['Concentratie_NORM'].apply(con_concentratie)
df_complete['fear_failure'] = df_complete['Faalangst_NORM'].apply(con_faalangst)
df_complete['test_strategies'] = df_complete['Teststrategieen_NORM'].apply(con_teststrategieen)
df_complete['pressure'] = df_complete['Pressure Pref_REC'].apply(con_pressure)
df_complete['cse'] = df_complete['CSE_RECODED'].apply(con_cse)

df_complete.info()
new_df = df_complete.iloc[:, 19:]

# converting variables
data_path = "/Users/davidfrost/Documents/chatbot_math/chatbot_program/data"
new_df.to_csv(os.path.join(data_path, "df_complete3.csv"), index=False)



df_sampled_math = df_math.groupby('level', group_keys=False).apply(lambda x: x.sample(frac=0.133333,replace=False))
df_sampled_math['level'].value_counts()
n_math = len(df_math)
n_sampled = len(df_sampled_math)
