
import pandas as pd
from shapely.geometry import Point
from _data_generation import DataGenerator
from _utils import _dist_matrix

class DataGeneratorFromDF(DataGenerator):
    """
    Use a lon/lat DataFrame for customer locations instead of random generation.
    Expects columns: 'lon', 'lat'.  Depot remains args['loc_depot'] = (lat, lon).
    """
    def __init__(self, args, customers_df: pd.DataFrame):
        self.args = dict(args)                    # do not mutate caller's dict
        self.df = customers_df.reset_index(drop=True).copy()

        # Update number of customers from the DataFrame
        self.args['I'] = len(self.df)

        # Build locations & distance matrix from DF
        self._construct_locations_from_df()

        # Reuse the original method to create demands, windows, and travel-time matrix.
        # If you have real (per-customer) demand/windows, you can override this too.
        self._generate_random_data()

        # For plotting (same as base class)
        import matplotlib.pyplot as plt
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)

    def _construct_locations_from_df(self):
        # Convert to (lat, lon) tuples expected by the repo
        self.loc_customers = [(row['lat'], row['lon']) for _, row in self.df.iterrows()]

        # All nodes: depot (lat, lon) first, then customers
        self.locations = [self.args['loc_depot']] + self.loc_customers

        # Distance matrix using geodesic miles (repo’s default)
        self.dist_matrix = _dist_matrix(self.locations)

        # Geo shapes for plotting (note shapely Point wants (lon, lat))
        self.geoms = [Point(lon, lat) for (lat, lon) in self.locations]
