import arcpy
import os


opj = os.path.join

output_path = r'C:\Users\anush\PycharmProjects\JakartaFlooding\output'
aprx = arcpy.mp.ArcGISProject(r'C:\Users\anush\PycharmProjects\JakartaFlooding\output\emptyproject.aprx')
m = aprx.listMaps("Map")[0]
years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
year = '2013'

m.addDataFromPath(r'C:\Users\anush\Downloads\BANJIR TAHUN 2013 - 2020\BANJIR TAHUN 2013 - 2020\BANJIR TAHUN 2013.shp')
l = m.listLayers('*')[0]

sym = l.symbology

sym.updateRenderer('GraduatedColorsRenderer')
months = [f'JAN_{year}', f'FEB_{year}', f'MAR_{year}', f'APRIL_{year}', f'MEI_{year}', f'JUN_{year}',
          f'JUL_{year}', f'AGU_{year}', f'OKT_{year}', f'NOV_{year}', f'DES_{year}']
for month in months:
    sym.renderer.classificationField = month
    sym.renderer.breakCount = 4
    sym.renderer.colorRamp = aprx.listColorRamps('Blues (Continuous)')[0]

    l.symbology = sym
    mv = m.defaultView
    mv.exportToPNG(opj(output_path, f'map_{month}.png'), width=1000, height=1000, world_file=True, color_mode="32-BIT_WITH_ALPHA")