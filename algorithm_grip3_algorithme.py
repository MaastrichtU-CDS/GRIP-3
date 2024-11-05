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
# inc. standaard populatie cijfers, op 1-1-2022 en op 31-12-2022

import pandas as pd
import os

# change working directory to the location of the files
# os.chdir('python/pht/20240923_PHT/')

# print the current working directory
print('Starting the script')
print()
print('Current working directory: ' + os.getcwd())

# define the file paths
file_paths = [
    'Patient.csv',
    'Episodes.csv',
    'Uitslagen.csv',
    'Populatie.csv',
]

# Make sure the data files exist
for file_path in file_paths:
    if not os.path.exists(file_path):
        print('File ' + file_path + ' does not exist')
        exit()

# Read the CSV files into pandas dataframes
dataframes = [pd.read_csv(file_path) for file_path in file_paths]

# Access individual dataframes
df_patient, df_episodes, df_uitslagen, df_populaties = dataframes

# Print the colum names of the 4 dataframe
print()
print('Columns of Patient.csv:   ', df_patient.columns.tolist())
print('Columns of Episodes.csv:  ', df_episodes.columns.tolist())
print('Columns of Uitslagen.csv: ', df_uitslagen.columns.tolist())
print('Columns of Populatie.csv: ', df_populaties.columns.tolist())

# change the datatype of the columns that contain a data to datetime
df_episodes['datum_start'] = pd.to_datetime(df_episodes['datum_start'], errors = 'coerce')
# print(df_episodes[df_episodes['datum_start'].isnull()])
df_uitslagen['datum'] = pd.to_datetime(df_uitslagen['datum'], errors = 'coerce')
# print(df_uitslagen[df_uitslagen['datum'].isnull()])
df_populaties['peildatum'] = pd.to_datetime(df_populaties['peildatum'], errors = 'coerce')
# print(df_populaties[df_populaties['peildatum'].isnull()])


# Prep: populatie cijfers
print()
print('Voorbereiding: bereken totale populatie cijfers voor alle praktijken')

# make new empty result dictionary
result = {}

# get populaties on 2022-01-01 and 2022-12-31
populatie_2022_01_01 = df_populaties.loc[df_populaties['peildatum'] == '2022-01-01'][['aantal']].sum().values[0]
print('totale populatie op 2022-01-01:   ', populatie_2022_01_01)
result['populatie_2022_01_01'] = populatie_2022_01_01

populatie_2022_12_31 = df_populaties.loc[df_populaties['peildatum'] == '2022-12-31'][['aantal']].sum().values[0]
print('totale populatie op 2022-12-31:   ', populatie_2022_12_31)
result['populatie_2022_12_31'] = populatie_2022_12_31

# calculate the midtime population
populatie_2022_gemiddeld = round((populatie_2022_12_31 + populatie_2022_01_01) / 2)
print('totale populatie 2022, gemiddeld: ', populatie_2022_gemiddeld)
result['populatie_2022_gemiddeld'] = populatie_2022_gemiddeld

# Vraag 1
print()
print('Vraag 1: Wat is de incidentie van apendicities (D88) en cholelithiasis (D98*)?')
print('         incidentie := episodes nieuw gestart in 2022')

# count episodes with icpc = D88
epi_d88 = df_episodes.loc[df_episodes['icpc1_code'].str.startswith('D88', na=False)]
count_epi_d88 = len(epi_d88)
print('aantal episodes D88: ', count_epi_d88)
result['count_epi_d88'] = count_epi_d88
incidentie_d88 = round(count_epi_d88 / populatie_2022_gemiddeld * 1000, 2)
print('incidentie D88 per 1000 patient jaren: ', incidentie_d88)
result['incidentie_d88'] = incidentie_d88

# count episodes with icpc = D98
epi_d98 = df_episodes.loc[df_episodes['icpc1_code'].str.startswith('D98', na=False)]
count_epi_d98 = len(epi_d98)
print('aantal episodes D98: ', count_epi_d98)
result['count_epi_d98'] = count_epi_d98
incidentie_d98 = round(count_epi_d98 / populatie_2022_gemiddeld * 1000 , 2)
print('incidentie D98 per 1000 patient jaren: ', incidentie_d98)
result['incidentie_d98'] = incidentie_d98


# Vraag 2
print()
print('Vraag 2: Wat is de incidentie en prevalencie van OMA (H71) otitis.. . EN UWI (U71*)?')
print('         incidentie := episodes nieuw gestart in 2022')
print('         puntprevalentie op 31-12-2022 := patienten met 8 weken ervoor t/m 31-12-2022 een nieuwe episode H71 of U71 (aanname: duur  8 weken)')

# count episodes with icpc = H71
epi_h71 = df_episodes.loc[df_episodes['icpc1_code'].str.startswith('H71', na=False)]
count_epi_h71 = len(epi_h71)
print('aantal episodes H71: ', count_epi_h71)
result['count_epi_h71'] = count_epi_h71
incidentie_h71 = round(count_epi_h71 / populatie_2022_gemiddeld * 1000, 2)
print('incidentie H71 per 1000 patient jaren: ', incidentie_h71)
result['incidentie_h71'] = incidentie_h71

# count patients with episiodes epi_h71 with start date between 2022-10-01 and 2022-12-31
epi_h71_prev = epi_h71[(epi_h71['datum_start'] >= '2022-10-01') & (epi_h71['datum_start'] <= '2022-12-31')]
count_pat_h71_prev = len(epi_h71_prev['pat_studie_id'].unique())
print('aantal patienten met H71 op 2022-12-31: ', count_pat_h71_prev)
result['count_pat_h71_prev'] = count_pat_h71_prev
prevalentie_h71_2022_12_31 = round(count_pat_h71_prev / populatie_2022_12_31 * 1000, 2)
print('puntprevalentie H71 op 2022-12-31 per 1000: ', prevalentie_h71_2022_12_31)
result['prevalentie_h71_2022_12_31'] = prevalentie_h71_2022_12_31

# count episodes with icpc = U71
epi_u71 = df_episodes.loc[df_episodes['icpc1_code'].str.startswith('U71', na=False)]
count_epi_u71 = len(epi_u71)
print('aantal episodes U71: ', count_epi_u71)
result['count_epi_u71'] = count_epi_u71
incidentie_u71 = round(count_epi_u71 / populatie_2022_gemiddeld * 1000, 2)
print('incidentie U71 per 1000 patient jaren: ', incidentie_u71)
result['incidentie_u71'] = incidentie_u71

# count patients with episiodes epi_u71 with start date between 2022-10-01 and 2022-12-31
epi_u71_prev = epi_u71[(epi_u71['datum_start'] >= '2022-10-01') & (epi_u71['datum_start'] <= '2022-12-31')]
count_pat_u71_prev = len(epi_u71_prev['pat_studie_id'].unique())
print('aantal patienten met U71 op 2022-12-31: ', count_pat_u71_prev)
result['count_pat_u71_prev'] = count_pat_u71_prev
prevalentie_u71_2022_12_31 = round(count_pat_u71_prev / populatie_2022_12_31 * 1000, 2)
print('puntprevalentie U71 op 2022-12-31 per 1000: ', prevalentie_u71_2022_12_31)
result['prevalentie_u71_2022_12_31'] = prevalentie_u71_2022_12_31


# Vraag 3
print()
print('Vraag 3: Wat is de gemiddelde BMI van mensen met DM2 (T90 en T90.02)')
print('         episodes diabetes type 2, gestart ooit t/m 1-1-2022; alle uitslagen van bepalingen lengte en gewicht in 2022')


# count episodes with icpc = T90
epi_t90 = df_episodes.loc[df_episodes['icpc1_code'].str.startswith('T90', na=False)]
count_epi_t90 = len(epi_t90)
print('aantal episodes T90 ooit: ', count_epi_t90)
result['count_epi_t90'] = count_epi_t90

# count patients with episiodes epi_t90
count_pat_t90 = len(epi_t90['pat_studie_id'].unique())
print('aantal patienten met T90 ooit: ', count_pat_t90)
result['count_pat_t90'] = count_pat_t90

# select uitslagen for pat_studie_id in epi_t90
uitslagen_t90 = df_uitslagen[df_uitslagen['pat_studie_id'].isin(epi_t90['pat_studie_id'])]
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
    (uitslagen_t90['bepaling_nr'] == 560)
    & (uitslagen_t90['waarde_numeriek'] >= 0.3)
    & (uitslagen_t90['waarde_numeriek'] <= 2.5)
    & (uitslagen_t90['datum'] >= '2022-01-01')
    & (uitslagen_t90['datum'] <= '2022-12-31')
    ]
uitslagen_t90_gewicht = uitslagen_t90[
    (uitslagen_t90['bepaling_nr'] == 357)
    & (uitslagen_t90['waarde_numeriek'] >= 20)
    & (uitslagen_t90['waarde_numeriek'] <= 300)
    & (uitslagen_t90['datum'] >= '2022-01-01')
    & (uitslagen_t90['datum'] <= '2022-12-31')
    ]

# select meest recente uitslag lengte per patient
lengte_recent = uitslagen_t90_lengte.sort_values('datum', ascending=False).drop_duplicates('pat_studie_id')[['pat_studie_id', 'waarde_numeriek']]
count_pat_t90_lengte = len(lengte_recent)
print ('aantal patienten met T90 met meting lengte: ', count_pat_t90_lengte)
result['count_pat_t90_lengte'] = count_pat_t90_lengte

# select meest recente uitslag gewicht per patient
gewicht_recent = uitslagen_t90_gewicht.sort_values('datum', ascending=False).drop_duplicates('pat_studie_id')[['pat_studie_id', 'waarde_numeriek']]
count_pat_t90_gewicht = len(gewicht_recent)
print ('aantal patienten met T90 met meting gewicht: ', count_pat_t90_gewicht)
result['count_pat_t90_gewicht'] = count_pat_t90_gewicht

# merge max lengte and max gewicht and change the labels to gewicht and lengte
pat_lengte_gewicht = pd.merge(lengte_recent, gewicht_recent, on='pat_studie_id', suffixes=('_lengte', '_gewicht'))
# select column pat_studie_id, waarde_numeriek_lengte and waarde_numeriek_gewicht

# calculate BMI
pat_lengte_gewicht['BMI'] = pat_lengte_gewicht['waarde_numeriek_gewicht' ] / (pat_lengte_gewicht['waarde_numeriek_lengte'] ** 2)
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
