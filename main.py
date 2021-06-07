import arcpy
import os


opj = os.path.join

stuff_path = r'C:\Users\anush\PycharmProjects\JakartaFlooding\stuff'
aprx = arcpy.mp.ArcGISProject(r'C:\Users\anush\PycharmProjects\JakartaFlooding\stuff\emptyproject.aprx')
m = aprx.listMaps("Map")[0]
m.addDataFromPath(r'C:\Users\anush\Downloads\BANJIR TAHUN 2013\BANJIR TAHUN 2013.shp')
l = m.listLayers('*')[0]

sym = l.symbology



# print('\n\n\n\n'.join([x.name for x in aprx.listColorRamps('*')]))
# if hasattr(sym, 'renderer'):
#   if sym.renderer.type == 'SimpleRenderer':
sym.updateRenderer('GraduatedColorsRenderer')
sym.renderer.classificationField = 'JAN_2013'
sym.renderer.breakCount = 4
sym.renderer.colorRamp = aprx.listColorRamps('Blues (Continuous)')[0]

l.symbology = sym


mv = m.defaultView
mv.exportToPNG(opj(stuff_path, 'out.png'), width=1000, height=1000, world_file=True, color_mode="32-BIT_WITH_ALPHA")