import pandas as pd
import numpy as np
from scipy.special import softmax
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data = {
    'customer_cc': ['John Doe CC'] * 6,
    'epsilon_record': ['Home Epsilon'] * 3 + ['Work Epsilon'] * 3,
    'store': ['San Antonio', 'Waco', 'Plano'] * 2,
    'weekly_store_sales': [800000, 400000, 1100000] * 2,
    'customer_sales_at_store': [20500, 2500, 75] * 2,
    'distance_to_store': [5, 170, 250, 315, 110, 11],  # Home: close to SA, far from others; Work: close to Plano, medium to Waco, far to SA
    'idf_store': [1.2, 1.5, 0.8] * 2,  # Assume IDF: log(N_total / N_at_store); higher for rarer stores
    'local_density': [3, 2, 1] * 2  # Number of nearby stores
}

df = pd.DataFrame(data)

# Total CC spend (sum across unique stores)
total_cc_spend = df['customer_sales_at_store'].unique().sum()  # 23075 in this example

# Original Gravity Score
def original_gravity(group):
    return np.sum(group['weekly_store_sales'] * group['customer_sales_at_store'] / group['distance_to_store']**2)

# Tuned Exponent (beta=1.5)
def tuned_gravity(group, beta=1.5):
    return np.sum(group['weekly_store_sales'] * group['customer_sales_at_store'] / group['distance_to_store']**beta)

# Normalized Gravity
def normalized_gravity(group, total_spend):
    grav = original_gravity(group)
    return grav / total_spend

# Soft-max Probability (across epsilon groups)
def softmax_prob(df):
    gravs = df.groupby('epsilon_record').apply(original_gravity)
    probs = softmax(list(gravs.values))
    return dict(zip(gravs.index, probs))

# Huff-Style Per-Store Probability (for a specific store, per epsilon)
def huff_per_store(df, store_name, beta=2):
    store_df = df[df['store'] == store_name]
    attract = store_df['weekly_store_sales'] / store_df['distance_to_store']**beta
    total_attract = attract.sum()
    probs = attract / total_attract
    spend_share = store_df['customer_sales_at_store'] / total_cc_spend
    return dict(zip(store_df['epsilon_record'], probs * spend_share))

# Commuter/Work Flag (simple rule: if sum for d>100 > 2x sum for d<=100, flag as work)
def commuter_flag(group):
    home_grav = np.sum(group[group['distance_to_store'] <= 100]['weekly_store_sales'] * group[group['distance_to_store'] <= 100]['customer_sales_at_store'] / group[group['distance_to_store'] <= 100]['distance_to_store']**2)
    work_grav = np.sum(group[group['distance_to_store'] > 100]['weekly_store_sales'] * group[group['distance_to_store'] > 100]['customer_sales_at_store'] / group[group['distance_to_store'] > 100]['distance_to_store']**2)
    return 'Work' if work_grav > 2 * home_grav else 'Home'

# Store-Density Adjustment
def density_adjusted_gravity(group):
    return np.sum((group['weekly_store_sales'] * group['customer_sales_at_store'] / group['distance_to_store']**2) * (1 / group['local_density']))

# TF-IDF Enhanced Gravity
def tfidf_gravity(group):
    return np.sum(group['weekly_store_sales'] * (group['customer_sales_at_store'] * group['idf_store']) / group['distance_to_store']**2)

# Location Entropy (simple mock: assume entropy per store, weight inversely)
# Mock entropy values (lower = more unique)
df['store_entropy'] = [0.5, 0.7, 0.9] * 2
def entropy_weighted_gravity(group):
    weights = 1 / (1 + group['store_entropy'])  # Inverse entropy for higher weight on unique
    return np.sum(group['weekly_store_sales'] * group['customer_sales_at_store'] * weights / group['distance_to_store']**2)

# ML Hybrid (simple example with mock labels)
# Aggregate features per epsilon
agg_df = df.groupby('epsilon_record').agg({
    'distance_to_store': 'mean',  # Example aggregated features
    'store': 'count'  # num_stores
}).rename(columns={'store': 'num_stores'})
grav_df = df.groupby('epsilon_record').apply(original_gravity).reset_index(name='gravity')
agg_df = agg_df.reset_index().merge(grav_df, on='epsilon_record')
agg_df['label'] = [1 if er == 'Home Epsilon' else 0 for er in agg_df['epsilon_record']]  # Mock: Home=1, Work=0

# Train simple model (LogisticRegression for small data)
features = ['gravity', 'num_stores', 'distance_to_store']
X = agg_df[features]
y = agg_df['label']
model = LogisticRegression()
model.fit(X, y)
preds = model.predict(X)
acc = accuracy_score(y, preds)  # 1.0 on this toy data; use validation in practice
