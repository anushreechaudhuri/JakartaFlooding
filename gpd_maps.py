import geopandas as gpd
import matplotlib.pyplot as plt
import os

from matplotlib import colors
from matplotlib.cm import ScalarMappable
from tqdm.auto import tqdm
import pdfplot

shape_dir = 'data'
shape_files = [os.path.join(shape_dir, filename) for filename in os.listdir(shape_dir) if '.shp' in filename]


def get_clean_data_map():
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

    clean_map = {

    }

    for year in years:
        shp = gpd.read_file([x for x in shape_files if str(year) in x][0])

        fields = list(shp.columns)
        mapping = {}

        for month in months:
            for month_possibility in month_possibilities[month]:
                field_possibilities = [f'BANJIR_{month_possibility}', f'{month_possibility}_{year}',
                                       f'{month_possibility}{year}',
                                       f'flood_{month_possibility}', f'{month_possibility}_{year % 100}',
                                       f'{month_possibility}', f'{month_possibility}{year % 100}',
                                       ] + [f'{month_possibility}_{str(year)[:i]}' for i in range(5)]
                field_possibilities = [x.upper() for x in field_possibilities] + [x.lower() for x in
                                                                                  field_possibilities]
                for field_poss in field_possibilities:
                    if field_poss in fields:
                        mapping[month] = field_poss
                        fields.remove(field_poss)
                        break
                if month in mapping: break
            if month not in mapping:
                clean_map[str(year)] = mapping

    return clean_map


clean_map = get_clean_data_map()


for year in tqdm(clean_map.keys(), desc='years'):
    for month in clean_map[year].keys():
        shp = gpd.read_file([x for x in shape_files if str(year) in x][0])

        fig, ax = pdfplot.make_fig()
        cmap = plt.get_cmap('Blues', 5)
        norm = colors.BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
        shp.plot(clean_map[year][month], ax=ax, cmap=cmap, vmin=0.5, edgecolor="black", linewidth=0.25)
        cax = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ticks=[1, 2, 3, 4, 5], orientation='horizontal')
        cax.set_label(f'Flood Depth \n Codes: 1 = 10-30 cm, 2 = 31-70cm, 3 = 71-50cm, 4 = 150+cm')
        cax.ax.tick_params(size=0)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.title(f'Jakarta Floods in {month} {year}', fontsize=18, weight='bold')
        plt.tight_layout()
        plt.savefig(f'gpd_maps/{year}_{month}.svg')
        plt.savefig(f'gpd_maps/{year}_{month}.png', dpi=300)
pdfplot.save_figs(folder='gpd_maps')  # magic
