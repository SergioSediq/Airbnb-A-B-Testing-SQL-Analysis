import pandas as pd
import numpy as np
import sqlite3
import os

# File paths
RAW_DATA_PATH = 'data/airbnb_raw.csv'
CLEAN_DATA_PATH = 'data/airbnb_clean.csv'
DB_PATH = 'data/airbnb_ab_test.db'

def clean_data(df):
    """Clean and prepare data for A/B testing"""
    print("\nCleaning data...")
    
    print(f"Initial rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Standardize column names
    column_mapping = {
        'id': 'listing_id',
        'NAME': 'name',
        'host id': 'host_id',
        'neighbourhood': 'neighborhood',
        'neighbourhood group': 'neighborhood_group',
        'room type': 'room_type',
        'price': 'price',
        'minimum nights': 'minimum_nights',
        'number of reviews': 'number_of_reviews',
        'reviews per month': 'reviews_per_month',
        'availability 365': 'availability_365',
        'instant_bookable': 'instant_bookable'
    }
    
    # Rename columns
    df = df.rename(columns=column_mapping)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['listing_id'])
    
    # Handle missing values in key columns
    df = df.dropna(subset=['price', 'room_type'])
    
    # Clean price (remove $ and commas, convert to float)
    if df['price'].dtype == 'object':
        df['price'] = df['price'].astype(str).str.replace('$', '').str.replace(',', '')
    df['price'] = pd.to_numeric(df['price'], errors='coerce').astype(float)  # <-- ADD .astype(float) HERE
    
    # Remove rows with invalid prices
    df = df[(df['price'] > 0) & (df['price'].notna())]
    
    # Remove outliers (price) using IQR method
    q1 = df['price'].quantile(0.25)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1
    df = df[(df['price'] >= q1 - 1.5 * iqr) & (df['price'] <= q3 + 1.5 * iqr)]
    
    # Fill missing numeric values
    df['minimum_nights'] = df['minimum_nights'].fillna(1)
    df['number_of_reviews'] = df['number_of_reviews'].fillna(0)
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    df['availability_365'] = df['availability_365'].fillna(365)
    
    # Convert instant_bookable to binary
    if 'instant_bookable' in df.columns:
        df['instant_bookable'] = df['instant_bookable'].map({'t': 1, 'f': 0}).fillna(0).astype(int)
    else:
        df['instant_bookable'] = 0
    
    # Feature engineering
    df['price_tier'] = pd.cut(df['price'], 
                               bins=[0, 100, 200, 500, float('inf')], 
                               labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
    
    df['has_reviews'] = (df['number_of_reviews'] > 0).astype(int)
    
    print(f"Final rows: {len(df)}")
    
    return df

def assign_ab_groups(df):
    """Randomly assign listings to control (A) vs treatment (B) groups"""
    print("\nAssigning A/B test groups...")
    
    rng = np.random.default_rng(42)
    
    # Random assignment (50/50 split)
    df['ab_group'] = rng.choice(['A', 'B'], size=len(df), p=[0.5, 0.5])
    
    # Simulate treatment effect
    df['booking_rate'] = rng.uniform(0.1, 0.4, len(df))
    
    # Apply treatment effect to group B
    treatment_mask = df['ab_group'] == 'B'
    df.loc[treatment_mask, 'booking_rate'] = df.loc[treatment_mask, 'booking_rate'] * 1.10
    df.loc[treatment_mask, 'price'] = (df.loc[treatment_mask, 'price'] * 1.05).astype(float)
    
    # Calculate bookings
    df['bookings'] = (df['booking_rate'] * df['availability_365']).astype(int)
    
    # Calculate revenue
    df['revenue'] = (df['bookings'] * df['price']).astype(float)
    
    group_counts = df['ab_group'].value_counts()
    print(f"Group A (Control): {group_counts['A']} listings")
    print(f"Group B (Treatment): {group_counts['B']} listings")
    
    return df

def save_to_database(df):
    """Save data to SQLite database"""
    print(f"\nSaving data to database: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('listings', conn, if_exists='replace', index=False)
    conn.close()
    
    print("Data saved to database successfully")

def save_cleaned_data(df):
    """Save cleaned data to CSV"""
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"\nCleaned data saved to {CLEAN_DATA_PATH}")
    
    # Print summary
    print("\nData Summary:")
    print(f"Total listings: {len(df)}")
    print(f"Average price: ${df['price'].mean():.2f}")
    print(f"Average bookings: {df['bookings'].mean():.1f}")
    print("\nBooking rate by group:")
    print(df.groupby('ab_group')['booking_rate'].mean())
    print("\nRoom type distribution:")
    print(df['room_type'].value_counts())

def main():
    """Main execution function"""
    print("Starting Airbnb A/B Testing Analysis...\n")
    
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: {RAW_DATA_PATH} not found!")
        return
    
    print("Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH, low_memory=False)
    
    df_clean = clean_data(df)
    df_ab = assign_ab_groups(df_clean)
    save_cleaned_data(df_ab)
    save_to_database(df_ab)
    
    print("\n" + "="*50)
    print("DATA PREPARATION COMPLETE")
    print("="*50)
    print("\nNext steps:")
    print("1. Run SQL queries in sql/ folder")
    print("2. Open Jupyter notebook for analysis")
    print("3. Create Power BI dashboard using airbnb_clean.csv")

if __name__ == "__main__":
    main()