import geopandas as gpd

import matplotlib.pyplot as plt
from shapely.affinity import scale
from shapely.geometry import Polygon

import numpy as np
from collections.abc import Iterable
from descartes import PolygonPatch
from numpy.random import choice


def plot_shape(shape, ax, **kwargs):
    ax.add_patch(PolygonPatch(shape, **kwargs))

def plot_shapes(shapes, ax, palette=None, **kwargs):
    if not isinstance(shapes, Iterable):
        shapes = [shapes]
    for shape in shapes:
        if palette is None:
            plot_shape(shape, ax, **kwargs)
        else:
            plot_shape(shape, ax, fc = choice(palette), **kwargs)


def plot_gdf(gdf, ax, **kwargs):
    
    field_name = kwargs['field']
    
    bounds = gdf.geometry.bounds
    minx_arr = bounds['minx']
    miny_arr = bounds['miny']
    maxx_arr = bounds['maxx']
    maxy_arr = bounds['maxy']
    
    min_x_of_gdf = np.min(minx_arr)
    max_x_of_gdf = np.max(maxx_arr)

    min_y_of_gdf = np.min(miny_arr)
    max_y_of_gdf = np.max(maxy_arr)
    
    background_geom = Polygon([
        (min_x_of_gdf, min_y_of_gdf),
        (min_x_of_gdf, max_y_of_gdf),
        (max_x_of_gdf, max_y_of_gdf),
        (max_x_of_gdf, min_y_of_gdf)
    ])
    background_geom = scale(background_geom, 2, 2)
    
    
    ax.axis('off')
    ax.axis('equal')
    ax.autoscale()
    ax.set_xlim(min_x_of_gdf, max_x_of_gdf)
    ax.set_ylim(min_y_of_gdf, max_y_of_gdf)
    
    ax.add_patch(PolygonPatch(background_geom, **drawing_kwargs['background']))

    for layer_name in gdf[field_name].unique():

        kwargs = drawing_kwargs[layer_name] if layer_name in drawing_kwargs else {}
        layer_gdf = gdf[gdf[field_name] == layer_name]
        shapes = layer_gdf.geometry
        if 'hatch_c' in kwargs:
            # 为了给hatch和边框绘制不同的颜色, 默认hatch和边框的颜色一致？
            plot_shapes(shapes, ax, lw = 0, ec = kwargs['hatch_c'], **{k:v for k,v in kwargs.items() if k not in ['lw', 'ec', 'hatch_c']})
            plot_shapes(shapes, ax, fill = False, **{k:v for k,v in kwargs.items() if k not in ['hatch_c', 'hatch', 'fill']})
        else:
            plot_shapes(shapes, ax, **kwargs)
    

if __name__ == '__main__':
    gdf = gpd.read_file('./sample_data/sample_land_use_circle.shp')
    drawing_kwargs = {
        'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
        
        'Water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'hatch': 'ooo...', 'hatch_c': '#85c9e6', 'lw': 0, 'zorder': 2},
        
        'Transportation': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 0.5, 'lw': 0.5, 'zorder': 2},
        
        'Others': {'fc': '#D2D68D', 'ec': '#AEB441', 'lw': .5, 'zorder': 3, 'hatch': 'ooo...'},
        
        'Farmland': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': .5, 'zorder': 3, 'hatch': 'ooo...'},
        'Field': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': .5, 'zorder': 3},
        
        'Special': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': .5, 'zorder': 3},
        
        'Forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': .5, 'hatch': 'ooo...', 'zorder': 3},
        'Grass': {'fc': '#8BB174', 'ec': '#2F3737', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': .5, 'zorder': 3},
        

        'Public': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        'Residential': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        'Industrial': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        'Commercial': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
    }
    fig, ax = plt.subplots(figsize = (8, 8), constrained_layout = True)
    plot_gdf(gdf, ax, field='major')
    plt.savefig('./test.png')