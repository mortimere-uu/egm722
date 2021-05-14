import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


plt.ion()

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# load datasets
counties = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\egm722\Week3\data_files\Counties.shp')
wards = gpd.read_file(r'C:\Users\Ed\Documents\GitHub\egm722\Week3\data_files\NI_Wards.shp')
# print(counties.crs) # check epsg
# print(counties.crs == wards.crs) # test if the crs is the same for wards and counties.
# print(counties) # shows table below, debug to see entire table

# try to print the results to the screen using the format method demonstrated in the workbook
# print(counties.head())

# load the necessary data here and transform to a UTM projection
counties = counties.to_crs(epsg=32629) # convert counties to UTM
wards = wards.to_crs(epsg=32629) # convert wards to UTM


# your analysis goes here...
sum_population = wards['Population'].sum() #calulcate total population from wards
print('{:.2f} total population'.format(sum_population)) # print total population
# print(wards.head())
# print(counties.head())

join = gpd.sjoin(counties, wards, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join
print(join) # show the joined table, appears to be duplicating/triplying data along county borders (total = 2213977)
join_population = join['Population'].sum() # find total population in join GeoDataFrame
print('{:} join population'.format(join_population))
print(join.groupby(['CountyName'])['Population'].sum()) # summarise population total by CountyName
print(sum_population / join_population) # check total population is same between GeoDataFrames


# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
myCRS = ccrs.UTM(29)
# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False


# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(county_outlines)
county_handles = generate_handles([''], ['none'], edge='r')

ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
plt.show()
fig.savefig('sample_map_egm.png', dpi=300, bbox_inches='tight')
