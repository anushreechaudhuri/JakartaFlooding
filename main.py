import arcpy
import os

opj = os.path.join

output_path = r'C:\Users\anush\PycharmProjects\JakartaFlooding\output'
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

month_possibilities = {'JAN': ['JAN', 'JNR'],
                       'FEB': ['FEB'],
                       'MAR': ['MAR', 'MARET', 'MARE'],
                       'APR': ['APR', 'APRIL', 'APRI'],
                       'MAY': ['MAY', 'MEI'],
                       'JUN': ['JUN'],
                       'JUL': ['JUL'],
                       'AUG': ['AGU', 'AGS', 'AGT'],
                       'SEP': ['SEP', 'SEPT'],
                       'OCT': ['OCT', 'OKT', 'OKTOBER'],
                       'NOV': ['NOV'],
                       'DEC': ['DES']}

for year in years:
    print('======================================================================================')
    shp_path = rf'C:\Users\anush\Downloads\BANJIR TAHUN 2013 - 2020\BANJIR TAHUN 2013 - 2020\BANJIR TAHUN {year}.shp'
    aprx = arcpy.mp.ArcGISProject(r'C:\Users\anush\PycharmProjects\JakartaFlooding\output\emptyproject.aprx')
    m = aprx.listMaps("Map")[0]
    m.addDataFromPath(shp_path)

    fields = [field.name for field in arcpy.ListFields(shp_path)]
    mapping = {}

    for month in months:
        for month_possibility in month_possibilities[month]:
            field_possibilities = [f'BANJIR_{month_possibility}', f'{month_possibility}_{year}',
                                   f'{month_possibility}{year}',
                                   f'flood_{month_possibility}', f'{month_possibility}_{year % 100}',
                                   f'{month_possibility}', f'{month_possibility}{year % 100}',
                                   ] + [f'{month_possibility}_{str(year)[:i]}' for i in range(5)]
            field_possibilities = [x.upper() for x in field_possibilities] + [x.lower() for x in field_possibilities]
            for field_poss in field_possibilities:
                if field_poss in fields:
                    mapping[month] = field_poss
                    fields.remove(field_poss)
                    break
            if month in mapping: break

        if month not in mapping:
            print(f'{month} not in {year} dataset :(')
        else:
            try:
                l = m.listLayers('*')[0]
                sym = l.symbology
                sym.updateRenderer('GraduatedColorsRenderer')
                sym.renderer.classificationField = mapping[month]
                sym.renderer.breakCount = 4
                sym.renderer.colorRamp = aprx.listColorRamps('Blues (Continuous)')[0]
                l.symbology = sym
                mv = m.defaultView
                mv.exportToPNG(opj(output_path, f'map_{year}_{month}.png'), width=1000, height=1000, world_file=True,
                               color_mode="32-BIT_WITH_ALPHA")
            except:
                print('Weird error with ' + f'{year}/{month}')
