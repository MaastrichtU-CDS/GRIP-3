# Primaire onderzoeksvragen
# 1. Wat is de incidentie van apendicities (D88=D88) en cholelithiasis (D98 / D98*)?	
#   - incidentie:=episodes nieuw gestart in 2022
# 2. Wat is de incidentie en prevalencie van OMA (H71=H71) otitis.. . EN UWI (U71 / U71*)?	
#   - incidentie:=episodes nieuw gestart in 2022; 
#   - puintprevalentie op 31-12-2022:= patienten met 8 weken ervoor t/m 31-12-2022 een nieuwe episode H71 of U71 (aanname: duur  8 weken)
# 3. Wat is de gemiddelde BMI van mensen met DM2 (T90, icpc1 T90.02 (en evtl. T90?); 
#   - episodes diabetes type 2, gestart ooit t/m 1-1-2022; 
#   - alle uitslagen van bepalingen lengte en gewicht in 2022
#
# Input is een gecombineert bestand met daarin alle geselecteerde episodes en uitslagen (zie specificatie)
# Ieder record bevat ook het totale populatie cijfer voor 2022. 
# Opmerking: 
# Het populatiecijfer op 1-1-2022 en op 31-12-2022 is gelijk omdat allen patienten die heel 2022 aanwezig zijn meedoen.
#

import pandas as pd
import os

# import the Path class from the pathlib module 
from pathlib import Path

# get path of current directory from the location of the current file
current_path = Path(__file__).parent

# change working directory to the location of the current path
os.chdir(current_path)


# print the current working directory
print('Start van het script')
print()
print('Huidige working directory: ' + os.getcwd())

# define the input file paths
file_paths = ['demo_combined_data.csv', ]

# Make sure the data files exist
for file_path in file_paths:
    if not os.path.exists(file_path):
        print('File ' + file_path + ' bestaat niet. Abort.')
        exit()

# Read the CSV files into pandas dataframes
dataframes = [pd.read_csv(file_path) for file_path in file_paths]


# Access individual dataframes
df_combined = dataframes[0]

# Print the colum names of the dataframe
print()
print('Kolomen:  ', df_combined.columns.tolist())

# change the datatype of the columns that contain a date string to pandas datetime
df_combined['episode_datum_start'] = pd.to_datetime(df_combined['episode_datum_start'], errors = 'coerce')
df_combined['uitslag_datum'] = pd.to_datetime(df_combined['uitslag_datum'], errors = 'coerce')


# Prep: Get population size by selecting the field 'populatie' from thew first row of the combined data
populatie = df_combined.iloc[0]['populatie']
print()
print('Populatie (geextraheert uit de eesrte rij van de data) : ', populatie)

# Vraag 1
print()
print('Vraag 1: Wat is de incidentie van apendicities (D88) en cholelithiasis (D98*)?')
print('         incidentie := episodes nieuw gestart in 2022')

result = {}

# count episodes with icpc = D88
epi_d88 = df_combined.loc[df_combined['episode_icpc'].str.startswith('D88', na=False)]
count_epi_d88 = len(epi_d88)
print('- aantal episodes D88: ', count_epi_d88)
result['count_epi_d88'] = count_epi_d88
incidentie_d88 = round(count_epi_d88 / populatie * 1000, 2)
print('- incidentie D88 per 1000 patient jaren: ', incidentie_d88)
result['incidentie_d88'] = incidentie_d88

# count episodes with icpc = D98
epi_d98 = df_combined.loc[df_combined['episode_icpc'].str.startswith('D98', na=False)]
count_epi_d98 = len(epi_d98)
print('aantal episodes D98: ', count_epi_d98)
result['count_epi_d98'] = count_epi_d98
incidentie_d98 = round(count_epi_d98 / populatie * 1000 , 2)
print('- incidentie D98 per 1000 patient jaren: ', incidentie_d98)
result['incidentie_d98'] = incidentie_d98

# Vraag 2
print()
print('Vraag 2: Wat is de incidentie en prevalencie van OMA (H71) otitis... EN UWI (U71*)?')
print('         incidentie := episodes nieuw gestart in 2022')
print('         puntprevalentie op 31-12-2022 := patienten met 8 weken ervoor t/m 31-12-2022 een nieuwe episode H71 of U71 (aanname: duur  8 weken)')

# count episodes with icpc = H71
epi_h71 = df_combined.loc[df_combined['episode_icpc'].str.startswith('H71', na=False)]
count_epi_h71 = len(epi_h71)
print('- aantal episodes H71: ', count_epi_h71)
result['count_epi_h71'] = count_epi_h71
incidentie_h71 = round(count_epi_h71 / populatie * 1000, 2)
print('- incidentie H71 per 1000 patient jaren: ', incidentie_h71)
result['incidentie_h71'] = incidentie_h71

# count patients with episiodes epi_h71 with start date between 2022-10-01 and 2022-12-31
epi_h71_prev = epi_h71[(epi_h71['episode_datum_start'] >= '2022-10-01') & (epi_h71['episode_datum_start'] <= '2022-12-31')]
count_pat_h71_prev = len(epi_h71_prev['pat_studie_id'].unique())
print('- aantal patienten met H71 op 2022-12-31: ', count_pat_h71_prev)
result['count_pat_h71_prev'] = count_pat_h71_prev
prevalentie_h71_2022_12_31 = round(count_pat_h71_prev / populatie * 1000, 2)
print('- puntprevalentie H71 op 2022-12-31 per 1000: ', prevalentie_h71_2022_12_31)
result['prevalentie_h71_2022_12_31'] = prevalentie_h71_2022_12_31

# count episodes with icpc = U71
epi_u71 = df_combined.loc[df_combined['episode_icpc'].str.startswith('U71', na=False)]
count_epi_u71 = len(epi_u71)
print('- aantal episodes U71: ', count_epi_u71)
result['count_epi_u71'] = count_epi_u71
incidentie_u71 = round(count_epi_u71 / populatie * 1000, 2)
print('- incidentie U71 per 1000 patient jaren: ', incidentie_u71)
result['incidentie_u71'] = incidentie_u71

# count patients with episiodes epi_u71 with start date between 2022-10-01 and 2022-12-31
epi_u71_prev = epi_u71[(epi_u71['episode_datum_start'] >= '2022-10-01') & (epi_u71['episode_datum_start'] <= '2022-12-31')]
count_pat_u71_prev = len(epi_u71_prev['pat_studie_id'].unique())
print('- aantal patienten met U71 op 2022-12-31: ', count_pat_u71_prev)
result['count_pat_u71_prev'] = count_pat_u71_prev
prevalentie_u71_2022_12_31 = round(count_pat_u71_prev / populatie * 1000, 2)
print('- puntprevalentie U71 op 2022-12-31 per 1000: ', prevalentie_u71_2022_12_31)
result['prevalentie_u71_2022_12_31'] = prevalentie_u71_2022_12_31

# Vraag 3
print()
print('Vraag 3: Wat is de gemiddelde BMI van mensen met DM2 (T90 en T90.02)')
print('         episodes diabetes type 2, gestart ooit t/m 1-1-2022; alle uitslagen van bepalingen lengte en gewicht in 2022')


# count episodes with icpc = T90 or T90.02


epi_t90 = df_combined.loc[df_combined['episode_icpc'].str.match('^(T90)|(T90\.02)$', na=False)]
epi_t90


# epi_t90 = df_combined.loc[df_combined['episode_icpc'].str.startswith('T90', na=False)]
count_epi_t90 = len(epi_t90)
print('aantal episodes T90 ooit: ', count_epi_t90)
result['count_epi_t90'] = count_epi_t90

# count patients with episiodes epi_t90
count_pat_t90 = len(epi_t90['pat_studie_id'].unique())
print('aantal patienten met T90 ooit: ', count_pat_t90)
result['count_pat_t90'] = count_pat_t90

# select uitslagen for pat_studie_id in epi_t90
uitslagen_t90 = df_combined[df_combined['pat_studie_id'].isin(epi_t90['pat_studie_id'])]
count_uitslagen_t90 = len(uitslagen_t90)
print('aantal uitslagen van patienten met T90: ', count_uitslagen_t90)
result['count_uitslagen_t90'] = count_uitslagen_t90

# count patients with uitslagen for T90
count_pat_uitslagen_t90 = len(uitslagen_t90['pat_studie_id'].unique())
print('aantal patienten met T90 met meting(en): ', count_pat_uitslagen_t90)
result['count_pat_uitslagen_t90'] = count_pat_uitslagen_t90

# select uitslagen for bepalingen lengte en gewicht, met datum in 2022
# filter lengte tussen 0.3m and 2.5m en gewicht tussen 20kg and 300kg
uitslagen_t90_lengte = uitslagen_t90[
    (uitslagen_t90['uitslag_bepaling_nr'] == 560) 
    & (uitslagen_t90['uitslag_waarde_numeriek'] >= 0.3) 
    & (uitslagen_t90['uitslag_waarde_numeriek'] <= 2.5) 
    & (uitslagen_t90['uitslag_datum'] >= '2022-01-01')
    & (uitslagen_t90['uitslag_datum'] <= '2022-12-31')
]
uitslagen_t90_gewicht = uitslagen_t90[
    (uitslagen_t90['uitslag_bepaling_nr'] == 357) 
    & (uitslagen_t90['uitslag_waarde_numeriek'] >= 20) 
    & (uitslagen_t90['uitslag_waarde_numeriek'] <= 300)
    & (uitslagen_t90['uitslag_datum'] >= '2022-01-01')
    & (uitslagen_t90['uitslag_datum'] <= '2022-12-31')
]

# select meest recente uitslag lengte per patient 
lengte_recent = uitslagen_t90_lengte.sort_values('uitslag_datum', ascending=False).drop_duplicates('pat_studie_id')[['pat_studie_id', 'uitslag_waarde_numeriek']]
count_pat_t90_lengte = len(lengte_recent)
print ('aantal patienten met T90 met meting lengte in 2022: ', count_pat_t90_lengte)
result['count_pat_t90_lengte'] = count_pat_t90_lengte

# select meest recente uitslag gewicht per patient 
gewicht_recent = uitslagen_t90_gewicht.sort_values('uitslag_datum', ascending=False).drop_duplicates('pat_studie_id')[['pat_studie_id', 'uitslag_waarde_numeriek']]
count_pat_t90_gewicht = len(gewicht_recent)
print ('aantal patienten met T90 met meting gewicht in 2022: ', count_pat_t90_gewicht)
result['count_pat_t90_gewicht'] = count_pat_t90_gewicht

# merge max lengte and max gewicht and change the labels to gewicht and lengte
pat_lengte_gewicht = pd.merge(lengte_recent, gewicht_recent, on='pat_studie_id', suffixes=('_lengte', '_gewicht'))
# select column pat_studie_id, waarde_numeriek_lengte and waarde_numeriek_gewicht

# calculate BMI
pat_lengte_gewicht['BMI'] = pat_lengte_gewicht['uitslag_waarde_numeriek_gewicht' ] / (pat_lengte_gewicht['uitslag_waarde_numeriek_lengte'] ** 2)
count_pat_t90_bmi = len(pat_lengte_gewicht)
print ('aantal patienten met T90 met BMI berekenbaar: ', count_pat_t90_bmi)
result['count_pat_t90_bmi'] = count_pat_t90_bmi

# calculate the average BMI
avg_bmi_pat_t90 = pat_lengte_gewicht['BMI'].mean().round(2)
print('gemiddelde BMI van patienten met T90: ', avg_bmi_pat_t90)
result['avg_bmi_pat_t90'] = avg_bmi_pat_t90
# print the result
print()
print('Resultaten:')
print('- Vraag 1.1:  incidentie D88 per 1000 patient jaren:      ', result['incidentie_d88'])
print('- Vraag 1.2:  incidentie D98 per 1000 patient jaren:      ', result['incidentie_d98'])
print('- Vraag 2.1a: incidentie H71 per 1000 patient jaren:      ', result['incidentie_h71'])
print('- Vraag 2.1b: puntprevalentie H71 op 2022-12-31 per 1000: ', result['prevalentie_h71_2022_12_31'])
print('- Vraag 2.2a: incidentie U71 per 1000 patient jaren:      ', result['incidentie_u71'])
print('- Vraag 2.2b: puntprevalentie U71 op 2022-12-31 per 1000: ', result['prevalentie_u71_2022_12_31'])
print('- Vraag 3:    gemiddelde BMI van patienten met T90:       ', result['avg_bmi_pat_t90'])
print()
print('Finished successfully.')