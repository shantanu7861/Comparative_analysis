import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from datetime import datetime

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Macy's Competitive Analysis",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS FOR MODERN UI ==========
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #E31837;
        --secondary-color: #0046BE;
        --background-dark: #1E1E1E;
        --card-background: #2D2D2D;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #E31837 0%, #0046BE 50%, #FFD700 100%);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 32px;
        box-shadow: 0 10px 30px rgba(227, 24, 55, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 45px;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 19px;
        margin-top: 12px;
        font-weight: 300;
    }
    
    /* Filter display styling */
    .filter-display {
        background: linear-gradient(135deg, #0046BE 0%, #002D72 100%);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 32px;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 70, 190, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .filter-display h3 {
        margin: 0 0 16px 0;
        font-size: 21px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    
    .filter-tag {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        padding: 8px 16px;
        border-radius: 25px;
        margin: 5px 5px 5px 0;
        font-size: 15px;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
    }
    
    /* Product card styling - Enhanced for Macy's */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        margin-bottom: 20px;
        border: 1px solid #e6e6e6;
        position: relative;
        overflow: hidden;
    }
    
    .product-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(227, 24, 55, 0.2);
        border-color: #E31837;
    }
    
    .product-image {
        border-radius: 10px;
        width: 100%;
        height: 280px;
        object-fit: contain;
        margin-bottom: 15px;
        background: #f8f8f8;
        padding: 10px;
        transition: transform 0.3s ease;
    }
    
    .product-card:hover .product-image {
        transform: scale(1.02);
    }
    
    .product-brand {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        color: #0046BE;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
        padding: 4px 10px;
        background: rgba(0, 70, 190, 0.1);
        border-radius: 15px;
        display: inline-block;
    }
    
    .product-title {
        font-size: 15px;
        font-weight: 600;
        margin-top: 5px;
        color: #1f2937;
        height: 45px;
        overflow: hidden;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    
    .product-price {
        color: #E31837;
        font-size: 22px;
        font-weight: 800;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .product-qty {
        font-size: 13px;
        color: #666;
        margin-top: 5px;
        padding: 3px 8px;
        background: #f0f0f0;
        border-radius: 10px;
        display: inline-block;
    }
    
    .product-rating {
        display: flex;
        align-items: center;
        gap: 5px;
        margin-top: 8px;
    }
    
    .rating-stars {
        color: #FFD700;
        font-size: 16px;
    }
    
    .rating-value {
        font-size: 14px;
        font-weight: 600;
        color: #666;
    }
    
    .product-badges {
        position: absolute;
        top: 15px;
        left: 15px;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    
    .badge {
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-best {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
    }
    
    .badge-value {
        background: linear-gradient(135deg, #2196F3, #0D47A1);
        color: white;
    }
    
    .badge-premium {
        background: linear-gradient(135deg, #9C27B0, #6A1B9A);
        color: white;
    }
    
    .product-links {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    
    .product-link {
        flex: 1;
        padding: 10px;
        background: linear-gradient(135deg, #E31837 0%, #C4142C 100%);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(227, 24, 55, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .product-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(227, 24, 55, 0.4);
        background: linear-gradient(135deg, #C4142C 0%, #A31024 100%);
    }
    
    .product-link-macy {
        background: linear-gradient(135deg, #0046BE 0%, #002D72 100%);
        box-shadow: 0 2px 8px rgba(0, 70, 190, 0.3);
    }
    
    .product-link-macy:hover {
        box-shadow: 0 4px 12px rgba(0, 70, 190, 0.4);
        background: linear-gradient(135deg, #002D72 0%, #001F4E 100%);
    }
    
    /* Brand column header */
    .brand-column-header {
        background: linear-gradient(135deg, #E31837 0%, #0046BE 100%);
        color: white;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(227, 24, 55, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .brand-column-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Price tag styling */
    .price-tag {
        position: relative;
        display: inline-block;
        padding: 8px 15px;
        background: linear-gradient(135deg, #E31837, #FF6B6B);
        color: white;
        border-radius: 25px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(227, 24, 55, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        background: white;
        border: 1px solid #e6e6e6;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #E31837, #0046BE);
        color: white;
        border-color: #E31837;
    }
    
    /* Grid layout for gallery */
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 25px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATA LOADING FUNCTION ==========
@st.cache_data
def load_data(file_path=None):
    """Load and preprocess the Excel data for Macy's"""
    try:
        if file_path is None:
            default_path = Path("macys_data.xlsx")
            if default_path.exists():
                df = pd.read_excel(default_path)
            else:
                return create_dummy_data()
        else:
            df = pd.read_excel(file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Standardize column names
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'image' in col_lower or 'img' in col_lower:
                column_mapping[col] = 'Image_URL'
            elif 'link' in col_lower or 'url' in col_lower:
                column_mapping[col] = 'Product_Link'
            elif 'qty' in col_lower or 'quantity' in col_lower:
                column_mapping[col] = 'Qty'
            elif 'title' in col_lower or 'name' in col_lower or 'product' in col_lower:
                column_mapping[col] = 'Title'
            elif 'brand' in col_lower:
                column_mapping[col] = 'Brand'
            elif 'current' in col_lower or 'price' in col_lower:
                column_mapping[col] = 'Current'
            elif 'rating' in col_lower or 'avg rating' in col_lower:
                column_mapping[col] = 'Avg Rating'
        
        df = df.rename(columns=column_mapping)
        
        # Check required columns
        required_columns = ['Product_Link', 'Image_URL', 'Qty', 'Title', 'Brand', 'Current', 'Avg Rating']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            st.info("Required columns: Product_Link, Image_URL, Qty, Title, Brand, Current, Avg Rating")
            return create_dummy_data()
        
        # Clean data
        df['Brand'] = df['Brand'].astype(str).str.strip()
        df['Title'] = df['Title'].astype(str).str.strip()
        
        # Convert price to numeric (USD)
        df['Current'] = pd.to_numeric(
            df['Current'].astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.replace('USD', '', regex=False)
            .str.strip(), 
            errors='coerce'
        ).fillna(0)
        
        # Convert Qty to numeric
        df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0).astype(int)
        
        # Convert Avg Rating to numeric
        df['Avg Rating'] = pd.to_numeric(df['Avg Rating'], errors='coerce').fillna(0)
        
        # Clean URLs
        df['Product_Link'] = df['Product_Link'].astype(str).str.strip()
        df['Image_URL'] = df['Image_URL'].astype(str).str.strip()
        
        # Remove rows with missing essential data
        df = df.dropna(subset=['Brand', 'Title', 'Current'])
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return create_dummy_data()

def create_dummy_data():
    """Create dummy data for Macy's demonstration"""
    np.random.seed(42)
    
    brands = ['Nike', 'Adidas', 'Levi\'s', 'Calvin Klein', 'Michael Kors', 'Tommy Hilfiger', 
              'Ralph Lauren', 'Coach', 'Kate Spade', 'Under Armour', 'Puma', 'Reebok']
    
    product_titles = [
        "Men's Classic Polo Shirt", "Women's Running Shoes", "Leather Crossbody Bag",
        "Men's Jeans - Straight Fit", "Women's Dress - Cocktail Length", 
        "Men's Sport Jacket", "Women's Handbag with Chain Strap", "Athletic Shorts",
        "Formal Dress Shirt", "Casual Sneakers", "Winter Parka", "Summer Dress",
        "Business Suit", "Casual T-Shirt", "Evening Gown", "Athletic Leggings",
        "Denim Jacket", "Formal Shoes", "Swimwear Set", "Active Hoodie"
    ]
    
    data = {
        'Product_Link': [f'https://www.macys.com/shop/product/{i:06d}' for i in range(100)],
        'Image_URL': [f'https://via.placeholder.com/400x500.png?text=Product+{i+1}' for i in range(100)],
        'Qty': np.random.randint(1, 1000, 100),
        'Title': np.random.choice(product_titles, 100),
        'Brand': np.random.choice(brands, 100),
        'Current': np.random.uniform(19.99, 499.99, 100).round(2),
        'Avg Rating': np.random.uniform(3.0, 5.0, 100).round(1)
    }
    
    return pd.DataFrame(data)

# ========== ANALYSIS FUNCTIONS ==========
def calculate_metrics(df, brands):
    """Calculate key metrics for selected brands"""
    metrics = {}
    
    for brand in brands:
        brand_data = df[df['Brand'] == brand]
        if len(brand_data) > 0:
            avg_price = brand_data['Current'].mean()
            total_qty = brand_data['Qty'].sum()
            avg_rating = brand_data['Avg Rating'].mean()
            
            metrics[brand] = {
                'avg_price': round(avg_price, 2),
                'min_price': brand_data['Current'].min(),
                'max_price': brand_data['Current'].max(),
                'total_products': len(brand_data),
                'total_qty': total_qty,
                'avg_qty_per_product': round(total_qty / len(brand_data), 1) if len(brand_data) > 0 else 0,
                'avg_rating': round(avg_rating, 1),
                'rating_count': len(brand_data[brand_data['Avg Rating'] > 0])
            }
        else:
            metrics[brand] = {
                'avg_price': 0,
                'min_price': 0,
                'max_price': 0,
                'total_products': 0,
                'total_qty': 0,
                'avg_qty_per_product': 0,
                'avg_rating': 0,
                'rating_count': 0
            }
    
    return metrics

def get_price_range_label(price):
    """Categorize price into ranges"""
    if price < 50:
        return "Budget ($0-50)"
    elif price < 100:
        return "Mid-Range ($50-100)"
    elif price < 200:
        return "Premium ($100-200)"
    else:
        return "Luxury ($200+)"

def get_rating_stars(rating):
    """Generate star rating HTML"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars_html = '★' * full_stars
    if half_star:
        stars_html += '½'
    stars_html += '☆' * empty_stars
    
    return stars_html

# ========== MAIN APP ==========
def main():
    # Set currency for Macy's USA
    currency = "$"
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛍️ Macy's Competitive Analysis Dashboard</h1>
        <p>Strategic pricing insights and inventory analysis for Macy's products</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Macy%27s_Logo.svg/2560px-Macy%27s_Logo.svg.png", width='stretch')
        st.markdown("### 📊 Dashboard Controls")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Macy's Excel File", 
            type=['xlsx', 'xls', 'csv'], 
            help="Upload your Macy's competitive data file"
        )
        
        st.markdown("---")
        
        # Load data
        if uploaded_file is not None:
            df = load_data(uploaded_file)
        else:
            df = load_data()
        
        if len(df) == 0:
            st.error("❌ No valid data loaded. Please check your Excel file format.")
            st.stop()
        
        st.success(f"✅ Loaded {len(df)} products from Macy's")
        
        # Brand Selection
        st.markdown("### 🏷️ Select Brands")
        all_brands = sorted(df['Brand'].unique().tolist())
        
        selected_brands = st.multiselect(
            "Choose brands to analyze",
            all_brands,
            default=all_brands[:6] if len(all_brands) >= 6 else all_brands,
            help="Select brands for competitive analysis"
        )
        
        if not selected_brands:
            st.warning("⚠️ Please select at least one brand")
            return
        
        st.markdown("---")
        
        # Price Range Filter
        st.markdown("### 💰 Price Range Filter")
        min_price = float(df['Current'].min())
        max_price = float(df['Current'].max())
        
        price_range = st.slider(
            "Select price range",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=10.0,
            format="$%.2f"
        )
        
        # Rating Filter
        st.markdown("### ⭐ Minimum Rating")
        min_rating = st.slider(
            "Minimum average rating",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            step=0.5,
            format="%.1f stars"
        )
        
        # Quantity Filter
        st.markdown("### 📦 Quantity Available")
        min_qty = st.number_input(
            "Minimum quantity available",
            min_value=0,
            max_value=int(df['Qty'].max()),
            value=0,
            step=10
        )
        
        st.markdown("---")
        
        # Apply filters
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brands)]
        filtered_df = filtered_df[
            (filtered_df['Current'] >= price_range[0]) & 
            (filtered_df['Current'] <= price_range[1])
        ]
        filtered_df = filtered_df[filtered_df['Avg Rating'] >= min_rating]
        filtered_df = filtered_df[filtered_df['Qty'] >= min_qty]
        
        st.markdown(f"**Filtered Results:** {len(filtered_df)} products")
        
        # Quick Stats
        if len(filtered_df) > 0:
            st.markdown("---")
            st.markdown("### 📈 Quick Stats")
            avg_price = filtered_df['Current'].mean()
            total_qty = filtered_df['Qty'].sum()
            avg_rating = filtered_df['Avg Rating'].mean()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Price", f"${avg_price:.2f}")
            with col2:
                st.metric("Total Qty", f"{total_qty:,}")
            with col3:
                st.metric("Avg Rating", f"{avg_rating:.1f}")

    # ========== FILTER DISPLAY ==========
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        return
    
    filter_text = f"""
    <div class="filter-display">
        <h3>🔍 Active Filters</h3>
        <span class="filter-tag">🏷️ Brands: {len(selected_brands)} selected</span>
        <span class="filter-tag">💰 Price: ${price_range[0]:.2f} - ${price_range[1]:.2f}</span>
        <span class="filter-tag">⭐ Min Rating: {min_rating} stars</span>
        <span class="filter-tag">📦 Min Qty: {min_qty}+ units</span>
    </div>
    """
    st.markdown(filter_text, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    # Calculate metrics
    metrics = calculate_metrics(filtered_df, selected_brands)
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📊 Key Metrics", "📈 Charts & Analysis", "🖼️ Product Gallery"])
    
    # ========== TAB 1: KEY METRICS ==========
    with tab1:
        st.markdown("### 🎯 Brand Performance Metrics")
        
        # Sort brands by average price in descending order
        sorted_brands = sorted(selected_brands, 
                             key=lambda x: metrics[x]['avg_price'], 
                             reverse=True)
        
        # Display metrics in columns
        cols = st.columns(min(4, len(sorted_brands)))
        
        for idx, brand in enumerate(sorted_brands):
            col_idx = idx % len(cols)
            if metrics[brand]['total_products'] > 0:
                with cols[col_idx]:
                    # Brand header with color based on price positioning
                    price_position = "🏆 Premium" if metrics[brand]['avg_price'] > filtered_df['Current'].mean() else "💎 Value"
                    
                    st.markdown(f"""
                    <div style="background: {'linear-gradient(135deg, #E31837, #C4142C)' if price_position == '🏆 Premium' else 'linear-gradient(135deg, #0046BE, #002D72)'}; 
                                color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center;">
                        <h4 style="margin: 0; font-size: 18px;">{brand}</h4>
                        <small>{price_position}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Key metrics
                    st.metric(
                        "Avg Price",
                        f"{currency}{metrics[brand]['avg_price']:.2f}",
                        delta=f"{((metrics[brand]['avg_price'] - filtered_df['Current'].mean()) / filtered_df['Current'].mean() * 100):.1f}% vs avg" 
                        if filtered_df['Current'].mean() > 0 else None
                    )
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Products", metrics[brand]['total_products'])
                    with col_b:
                        st.metric("Total Qty", f"{metrics[brand]['total_qty']:,}")
                    
                    st.metric(
                        "Avg Rating",
                        f"{metrics[brand]['avg_rating']:.1f}",
                        help=f"Based on {metrics[brand]['rating_count']} ratings"
                    )
                    
                    st.markdown(f"""
                    <small style="color: #666;">
                        Price Range: {currency}{metrics[brand]['min_price']:.2f} - {currency}{metrics[brand]['max_price']:.2f}<br>
                        Avg Qty/Product: {metrics[brand]['avg_qty_per_product']}
                    </small>
                    """, unsafe_allow_html=True)
        
        # Summary Statistics
        st.markdown("---")
        st.markdown("### 📈 Overall Market Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Products", len(filtered_df))
        with col2:
            st.metric("Total Inventory", f"{filtered_df['Qty'].sum():,}")
        with col3:
            st.metric("Market Avg Price", f"${filtered_df['Current'].mean():.2f}")
        with col4:
            st.metric("Avg Market Rating", f"{filtered_df['Avg Rating'].mean():.1f}")
    
    # ========== TAB 2: CHARTS & ANALYSIS ==========
    with tab2:
        st.markdown("### 📊 Visual Analysis")
        
        # Price Distribution by Brand (Box Plot)
        st.markdown("#### 💰 Price Distribution by Brand")
        
        # Sort brands by median price
        brand_medians = []
        for brand in selected_brands:
            brand_data = filtered_df[filtered_df['Brand'] == brand]
            if len(brand_data) > 0:
                median_price = brand_data['Current'].median()
                brand_medians.append((brand, median_price))
        
        sorted_brand_medians = sorted(brand_medians, key=lambda x: x[1], reverse=True)
        sorted_brands_box = [brand for brand, median in sorted_brand_medians]
        
        fig_box = go.Figure()
        
        for brand in sorted_brands_box:
            brand_data = filtered_df[filtered_df['Brand'] == brand]
            
            fig_box.add_trace(go.Box(
                y=brand_data['Current'],
                name=brand,
                marker=dict(
                    color='#E31837' if brand == sorted_brands_box[0] else '#0046BE',
                    size=8
                ),
                boxmean='sd',
                hoverinfo='y+name'
            ))
        
        fig_box.update_layout(
            height=500,
            xaxis_title="Brand",
            yaxis_title="Price ($)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            showlegend=False,
            margin=dict(t=40, b=80, l=60, r=40),
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                zeroline=False,
                tickprefix="$"
            ),
            xaxis=dict(
                tickangle=45
            )
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Price vs Rating Scatter Plot
        st.markdown("---")
        st.markdown("#### ⭐ Price vs Rating Analysis")
        
        fig_scatter = px.scatter(
            filtered_df,
            x='Current',
            y='Avg Rating',
            color='Brand',
            size='Qty',
            hover_name='Title',
            hover_data=['Brand', 'Current', 'Avg Rating', 'Qty'],
            color_discrete_sequence=px.colors.qualitative.Set3,
            labels={'Current': 'Price ($)', 'Avg Rating': 'Average Rating'},
            title="Price vs Rating Distribution"
        )
        
        fig_scatter.update_traces(
            marker=dict(line=dict(width=1, color='DarkSlateGrey')),
            selector=dict(mode='markers')
        )
        
        fig_scatter.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                tickprefix="$"
            ),
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                range=[0, 5.5]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Brand Comparison Bar Chart
        st.markdown("---")
        st.markdown("#### 📊 Brand Comparison")
        
        comparison_data = []
        for brand in selected_brands:
            if brand in metrics:
                comparison_data.append({
                    'Brand': brand,
                    'Avg Price': metrics[brand]['avg_price'],
                    'Avg Rating': metrics[brand]['avg_rating'],
                    'Total Products': metrics[brand]['total_products'],
                    'Total Qty': metrics[brand]['total_qty']
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Create subplots
        fig_comparison = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Price ($)', 'Average Rating', 'Total Products', 'Total Quantity'),
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # Add traces
        fig_comparison.add_trace(
            go.Bar(
                x=comparison_df['Brand'],
                y=comparison_df['Avg Price'],
                name='Avg Price',
                marker_color='#E31837'
            ),
            row=1, col=1
        )
        
        fig_comparison.add_trace(
            go.Bar(
                x=comparison_df['Brand'],
                y=comparison_df['Avg Rating'],
                name='Avg Rating',
                marker_color='#0046BE'
            ),
            row=1, col=2
        )
        
        fig_comparison.add_trace(
            go.Bar(
                x=comparison_df['Brand'],
                y=comparison_df['Total Products'],
                name='Total Products',
                marker_color='#FFD700'
            ),
            row=2, col=1
        )
        
        fig_comparison.add_trace(
            go.Bar(
                x=comparison_df['Brand'],
                y=comparison_df['Total Qty'],
                name='Total Qty',
                marker_color='#4CAF50'
            ),
            row=2, col=2
        )
        
        fig_comparison.update_layout(
            height=700,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=100, b=80, l=60, r=40)
        )
        
        fig_comparison.update_xaxes(tickangle=45)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Top Performing Products
        st.markdown("---")
        st.markdown("#### 🏆 Top Performing Products")
        
        # Sort by different criteria
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Highest Rated**")
            top_rated = filtered_df.nlargest(5, 'Avg Rating')[['Title', 'Brand', 'Avg Rating', 'Current']]
            for idx, row in top_rated.iterrows():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #4CAF50;">
                    <strong>{row['Brand']}</strong><br>
                    <small>{row['Title'][:40]}...</small><br>
                    ⭐ {row['Avg Rating']} | ${row['Current']:.2f}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Best Value (Price/Rating)**")
            filtered_df['Value_Score'] = filtered_df['Avg Rating'] / filtered_df['Current'].clip(lower=1)
            best_value = filtered_df.nlargest(5, 'Value_Score')[['Title', 'Brand', 'Avg Rating', 'Current']]
            for idx, row in best_value.iterrows():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #2196F3;">
                    <strong>{row['Brand']}</strong><br>
                    <small>{row['Title'][:40]}...</small><br>
                    ⭐ {row['Avg Rating']} | ${row['Current']:.2f}
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("**Highest Inventory**")
            top_qty = filtered_df.nlargest(5, 'Qty')[['Title', 'Brand', 'Qty', 'Current']]
            for idx, row in top_qty.iterrows():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #FF9800;">
                    <strong>{row['Brand']}</strong><br>
                    <small>{row['Title'][:40]}...</small><br>
                    📦 {row['Qty']:,} | ${row['Current']:.2f}
                </div>
                """, unsafe_allow_html=True)
    
    # ========== TAB 3: PRODUCT GALLERY ==========
    with tab3:
        st.markdown("### 🖼️ Product Gallery")
        
        # Gallery controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox(
                "Sort products by",
                ['Price (High to Low)', 'Price (Low to High)', 'Rating (High to Low)', 
                 'Quantity (High to Low)', 'Brand A-Z', 'Brand Z-A']
            )
        
        with col2:
            products_per_page = st.selectbox(
                "Products per page",
                [12, 24, 36, 48],
                index=0
            )
        
        with col3:
            view_mode = st.selectbox(
                "View mode",
                ['Grid View', 'List View', 'Brand View'],
                index=0
            )
        
        # Sort the data
        gallery_df = filtered_df.copy()
        
        if sort_by == 'Price (High to Low)':
            gallery_df = gallery_df.sort_values('Current', ascending=False)
        elif sort_by == 'Price (Low to High)':
            gallery_df = gallery_df.sort_values('Current', ascending=True)
        elif sort_by == 'Rating (High to Low)':
            gallery_df = gallery_df.sort_values('Avg Rating', ascending=False)
        elif sort_by == 'Quantity (High to Low)':
            gallery_df = gallery_df.sort_values('Qty', ascending=False)
        elif sort_by == 'Brand A-Z':
            gallery_df = gallery_df.sort_values('Brand', ascending=True)
        elif sort_by == 'Brand Z-A':
            gallery_df = gallery_df.sort_values('Brand', ascending=False)
        
        # Pagination
        total_products = len(gallery_df)
        total_pages = (total_products + products_per_page - 1) // products_per_page
        
        if total_pages > 1:
            page = st.number_input(
                f"Page (1-{total_pages})",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1
            )
        else:
            page = 1
        
        start_idx = (page - 1) * products_per_page
        end_idx = min(start_idx + products_per_page, total_products)
        page_df = gallery_df.iloc[start_idx:end_idx]
        
        st.markdown(f"**Showing {start_idx + 1}-{end_idx} of {total_products} products**")
        
        if view_mode == 'Grid View':
            # Grid layout
            cols = st.columns(4)
            for idx, (_, product) in enumerate(page_df.iterrows()):
                col_idx = idx % 4
                with cols[col_idx]:
                    # Determine badge based on criteria
                    badges = []
                    if product['Current'] > filtered_df['Current'].mean() * 1.2:
                        badges.append(('badge-premium', 'PREMIUM'))
                    elif product['Avg Rating'] >= 4.5:
                        badges.append(('badge-best', 'TOP RATED'))
                    elif product['Qty'] > filtered_df['Qty'].median() * 2:
                        badges.append(('badge-value', 'HIGH STOCK'))
                    
                    # Product card
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    # Badges
                    if badges:
                        badge_html = '<div class="product-badges">'
                        for badge_class, badge_text in badges:
                            badge_html += f'<div class="badge {badge_class}">{badge_text}</div>'
                        badge_html += '</div>'
                        st.markdown(badge_html, unsafe_allow_html=True)
                    
                    # Image
                    image_url = str(product.get('Image_URL', '')).strip()
                    if image_url and image_url != 'nan' and image_url.startswith(('http://', 'https://')):
                        try:
                            st.image(image_url, use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x400.png?text=Product+Image", 
                                   use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x400.png?text=Macy%27s+Product", 
                               use_container_width=True)
                    
                    # Brand
                    st.markdown(f"<div class='product-brand'>{product['Brand']}</div>", unsafe_allow_html=True)
                    
                    # Title
                    title = product['Title'][:60] + ('...' if len(product['Title']) > 60 else '')
                    st.markdown(f"<div class='product-title'>{title}</div>", unsafe_allow_html=True)
                    
                    # Price
                    st.markdown(f"<div class='product-price'>{currency}{product['Current']:.2f}</div>", unsafe_allow_html=True)
                    
                    # Quantity
                    if product['Qty'] > 0:
                        qty_text = f"In Stock: {product['Qty']:,}"
                        if product['Qty'] < 50:
                            qty_text += " 🔥"
                        st.markdown(f"<div class='product-qty'>{qty_text}</div>", unsafe_allow_html=True)
                    
                    # Rating
                    if product['Avg Rating'] > 0:
                        stars = get_rating_stars(product['Avg Rating'])
                        st.markdown(f"""
                        <div class='product-rating'>
                            <span class='rating-stars'>{stars}</span>
                            <span class='rating-value'>{product['Avg Rating']:.1f}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Links
                    st.markdown('<div class="product-links">', unsafe_allow_html=True)
                    product_link = str(product.get('Product_Link', '')).strip()
                    if product_link and product_link != 'nan' and product_link.startswith('http'):
                        st.markdown(f'<a href="{product_link}" target="_blank" class="product-link">View Product</a>', 
                                  unsafe_allow_html=True)
                    else:
                        st.markdown(f'<button class="product-link" disabled>No Link</button>', 
                                  unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        elif view_mode == 'Brand View':
            # Group by brand
            for brand in sorted(selected_brands):
                brand_products = page_df[page_df['Brand'] == brand]
                if len(brand_products) > 0:
                    st.markdown(f"""
                    <div class="brand-column-header">
                        {brand} - {len(brand_products)} products
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display brand products in a grid
                    brand_cols = st.columns(4)
                    for idx, (_, product) in enumerate(brand_products.iterrows()):
                        col_idx = idx % 4
                        with brand_cols[col_idx]:
                            # Simplified product card for brand view
                            st.markdown('<div class="product-card">', unsafe_allow_html=True)
                            
                            # Image
                            image_url = str(product.get('Image_URL', '')).strip()
                            if image_url and image_url != 'nan' and image_url.startswith(('http://', 'https://')):
                                try:
                                    st.image(image_url, use_container_width=True)
                                except:
                                    st.image("https://via.placeholder.com/300x400.png?text=Product", 
                                           use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/300x400.png?text=Image", 
                                       use_container_width=True)
                            
                            # Title and price
                            title = product['Title'][:50] + ('...' if len(product['Title']) > 50 else '')
                            st.markdown(f"<div class='product-title'>{title}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-price'>{currency}{product['Current']:.2f}</div>", 
                                      unsafe_allow_html=True)
                            
                            # Quick info
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown(f"⭐ {product['Avg Rating']:.1f}")
                            with col_b:
                                st.markdown(f"📦 {product['Qty']}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
        
        else:  # List View
            for _, product in page_df.iterrows():
                cols = st.columns([1, 3, 1, 1, 1])
                
                with cols[0]:
                    image_url = str(product.get('Image_URL', '')).strip()
                    if image_url and image_url != 'nan' and image_url.startswith(('http://', 'https://')):
                        try:
                            st.image(image_url, width=80)
                        except:
                            st.image("https://via.placeholder.com/80x80.png?text=IMG", width=80)
                    else:
                        st.image("https://via.placeholder.com/80x80.png?text=N/A", width=80)
                
                with cols[1]:
                    st.markdown(f"**{product['Brand']}**")
                    st.markdown(f"{product['Title'][:70]}{'...' if len(product['Title']) > 70 else ''}")
                    if product['Avg Rating'] > 0:
                        stars = get_rating_stars(product['Avg Rating'])
                        st.markdown(f"<small>{stars} {product['Avg Rating']:.1f}</small>", unsafe_allow_html=True)
                
                with cols[2]:
                    st.markdown(f"**{currency}{product['Current']:.2f}**")
                
                with cols[3]:
                    st.markdown(f"📦 {product['Qty']:,}")
                
                with cols[4]:
                    product_link = str(product.get('Product_Link', '')).strip()
                    if product_link and product_link != 'nan' and product_link.startswith('http'):
                        st.markdown(f'<a href="{product_link}" target="_blank" class="product-link" style="padding: 5px 10px; font-size: 12px;">View</a>', 
                                  unsafe_allow_html=True)
                
                st.markdown("---")
        
        # Pagination controls at bottom
        if total_pages > 1:
            st.markdown(f"**Page {page} of {total_pages}**")
            cols = st.columns(5)
            with cols[2]:
                if page > 1:
                    if st.button("◀ Previous"):
                        st.rerun()
            with cols[3]:
                if page < total_pages:
                    if st.button("Next ▶"):
                        st.rerun()

if __name__ == "__main__":
    main()
