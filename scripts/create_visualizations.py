import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Paths
CLEAN_DATA_PATH = 'data/airbnb_clean.csv'
OUTPUT_DIR = 'visualizations'
REVENUE_LABEL = 'Revenue ($)'
PRICE_LABEL = 'Price ($)'

def load_data():
    """Load cleaned A/B test data"""
    print("Loading data...")
    df = pd.read_csv(CLEAN_DATA_PATH)
    print(f"Loaded {len(df)} records")
    return df

def create_output_dir():
    """Create visualizations directory"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_ab_comparison(df):
    """Create A/B group comparison bar chart"""
    print("Creating A/B comparison chart...")
    
    metrics = df.groupby('ab_group').agg({
        'booking_rate': 'mean',
        'revenue': 'mean',
        'price': 'mean'
    }).reset_index()
    
    _, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Booking Rate
    axes[0].bar(metrics['ab_group'], metrics['booking_rate'], 
                color=['#2196F3', '#F44336'], alpha=0.8)
    axes[0].set_title('Average Booking Rate', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Booking Rate')
    axes[0].set_xlabel('Group')
    
    # Revenue
    axes[1].bar(metrics['ab_group'], metrics['revenue'], 
                color=['#2196F3', '#F44336'], alpha=0.8)
    axes[1].set_title('Average Revenue', fontsize=14, fontweight='bold')
    axes[1].set_ylabel(REVENUE_LABEL)
    axes[1].set_xlabel('Group')
    
    # Price
    axes[2].bar(metrics['ab_group'], metrics['price'], 
                color=['#2196F3', '#F44336'], alpha=0.8)
    axes[2].set_title('Average Price', fontsize=14, fontweight='bold')
    axes[2].set_ylabel(PRICE_LABEL)
    axes[2].set_xlabel('Group')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/ab_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/ab_comparison.png")

def plot_room_type_distribution(df):
    """Create room type distribution charts"""
    print("Creating room type distribution...")
    
    _, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Overall distribution
    room_counts = df['room_type'].value_counts()
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
    
    # Create pie chart with percentages inside
    _, _, autotexts = axes[0].pie(
        room_counts, 
        autopct='%1.1f%%',
        colors=colors, 
        startangle=90,
        pctdistance=0.75  # Position percentages inside slices
    )
    
    # Make percentage text white and bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    # Add legend on the right side
    axes[0].legend(room_counts.index, 
                   loc='center left', 
                   bbox_to_anchor=(1, 0.5),
                   fontsize=10)
    axes[0].set_title('Room Type Distribution', fontsize=14, fontweight='bold')
    
    # By A/B group
    room_ab = df.groupby(['room_type', 'ab_group']).size().unstack()
    room_ab.plot(kind='bar', ax=axes[1], color=['#2196F3', '#F44336'], alpha=0.8)
    axes[1].set_title('Room Types by A/B Group', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Room Type')
    axes[1].set_ylabel('Count')
    axes[1].legend(title='Group')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/room_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/room_type_distribution.png")

def plot_revenue_distribution(df):
    """Create revenue distribution comparison"""
    print("Creating revenue distribution...")
    
    _, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram
    group_a = df[df['ab_group'] == 'A']['revenue']
    group_b = df[df['ab_group'] == 'B']['revenue']
    
    axes[0].hist(group_a, bins=50, alpha=0.7, label='Group A', color='#2196F3')
    axes[0].hist(group_b, bins=50, alpha=0.7, label='Group B', color='#F44336')
    axes[0].set_title('Revenue Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel(REVENUE_LABEL)
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    
    # Box plot
    df.boxplot(column='revenue', by='ab_group', ax=axes[1])
    axes[1].set_title('Revenue by Group', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Group')
    axes[1].set_ylabel(REVENUE_LABEL)
    plt.suptitle('')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/revenue_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/revenue_distribution.png")

def plot_neighborhood_performance(df):
    """Create top neighborhoods chart"""
    print("Creating neighborhood performance chart...")
    
    top_neighborhoods = df.groupby('neighborhood').agg({
        'listing_id': 'count',
        'revenue': 'mean'
    }).sort_values('revenue', ascending=False).head(10)
    
    _, axis = plt.subplots(figsize=(12, 6))
    
    x_positions = np.arange(len(top_neighborhoods))
    axis.barh(x_positions, top_neighborhoods['revenue'], color='#4CAF50', alpha=0.8)
    axis.set_yticks(x_positions)
    axis.set_yticklabels(top_neighborhoods.index)
    axis.set_xlabel('Average Revenue ($)', fontsize=12)
    axis.set_title('Top 10 Neighborhoods by Revenue', fontsize=14, fontweight='bold')
    axis.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/neighborhood_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/neighborhood_performance.png")

def plot_price_tier_analysis(df):
    """Create price tier analysis"""
    print("Creating price tier analysis...")
    
    _, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Price tier distribution
    price_tier_counts = df['price_tier'].value_counts()
    tier_colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
    axes[0].bar(price_tier_counts.index, price_tier_counts.values, 
                color=tier_colors, alpha=0.8)
    axes[0].set_title('Listings by Price Tier', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Price Tier')
    axes[0].set_ylabel('Count')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
    
    # Revenue by price tier
    price_revenue = df.groupby('price_tier')['revenue'].sum().sort_values(ascending=False)
    axes[1].bar(price_revenue.index, price_revenue.values, 
                color=tier_colors, alpha=0.8)
    axes[1].set_title('Total Revenue by Price Tier', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Price Tier')
    axes[1].set_ylabel('Total Revenue ($)')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/price_tier_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/price_tier_analysis.png")

def plot_statistical_summary(df):
    """Create statistical summary dashboard"""
    print("Creating statistical summary...")
    
    # Calculate metrics
    group_a = df[df['ab_group'] == 'A']
    group_b = df[df['ab_group'] == 'B']
    
    lift_booking = ((group_b['booking_rate'].mean() - group_a['booking_rate'].mean()) / 
                    group_a['booking_rate'].mean() * 100)
    lift_revenue = ((group_b['revenue'].mean() - group_a['revenue'].mean()) / 
                    group_a['revenue'].mean() * 100)
    
    _, axis = plt.subplots(figsize=(10, 6))
    axis.axis('off')
    
    summary_text = f"""
    A/B TEST RESULTS SUMMARY
    {'='*50}
    
    Total Listings: {len(df):,}
    Group A (Control): {len(group_a):,}
    Group B (Treatment): {len(group_b):,}
    
    BOOKING RATE:
    Group A: {group_a['booking_rate'].mean():.4f}
    Group B: {group_b['booking_rate'].mean():.4f}
    Lift: {lift_booking:+.2f}%
    
    REVENUE:
    Group A: ${group_a['revenue'].mean():.2f}
    Group B: ${group_b['revenue'].mean():.2f}
    Lift: {lift_revenue:+.2f}%
    
    PRICE:
    Group A: ${group_a['price'].mean():.2f}
    Group B: ${group_b['price'].mean():.2f}
    
    ROOM TYPES:
    {df['room_type'].value_counts().to_string()}
    """
    
    axis.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
              verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/statistical_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/statistical_summary.png")

def main():
    """Main execution function"""
    print("Starting A/B Test Visualization Generation...\n")
    
    # Create output directory
    create_output_dir()
    
    # Load data
    df = load_data()
    
    # Generate all visualizations
    plot_ab_comparison(df)
    plot_room_type_distribution(df)
    plot_revenue_distribution(df)
    plot_neighborhood_performance(df)
    plot_price_tier_analysis(df)
    plot_statistical_summary(df)
    
    print("\n" + "="*50)
    print("VISUALIZATION GENERATION COMPLETE")
    print("="*50)
    print(f"\nAll visualizations saved to: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    print("  - ab_comparison.png")
    print("  - room_type_distribution.png")
    print("  - revenue_distribution.png")
    print("  - neighborhood_performance.png")
    print("  - price_tier_analysis.png")
    print("  - statistical_summary.png")

if __name__ == "__main__":
    main()