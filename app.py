import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Competitive Analysis Dashboard",
    page_icon="👠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS FOR MODERN UI ==========
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #FF6B9D;
        --secondary-color: #4A90E2;
        --background-dark: #1E1E1E;
        --card-background: #2D2D2D;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 300;
    }
    
    /* Filter display styling */
    .filter-display {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .filter-display h3 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    
    .filter-tag {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.3rem 0.3rem 0.3rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Product card styling */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .product-image {
        border-radius: 10px;
        width: 100%;
        height: 220px;
        object-fit: cover;
        margin-bottom: 0.8rem;
    }
    
    .product-brand {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #8b5cf6;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .product-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.3rem;
        color: #1f2937;
        height: 40px;
        overflow: hidden;
        line-height: 1.3;
    }
    
    .product-price {
        color: #6366f1;
        font-size: 1.3rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }
    
    .product-category {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-style: italic;
    }
    
    .product-link {
        display: inline-block;
        margin-top: 0.6rem;
        padding: 0.6rem 1.2rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    .product-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Brand column header */
    .brand-column-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATA LOADING FUNCTION ==========
@st.cache_data
def load_data(file_path=None):
    """Load and preprocess the Excel data"""
    try:
        if file_path is None:
            default_path = Path("ka.xlsx")
            if default_path.exists():
                df = pd.read_excel(default_path, sheet_name="Sheet1")
            else:
                return create_dummy_data()
        else:
            df = pd.read_excel(file_path, sheet_name="Sheet1")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Standardize column names
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'image' in col_lower or 'img' in col_lower or 'url' in col_lower:
                column_mapping[col] = 'Image_URL'
            elif 'price' in col_lower:
                column_mapping[col] = 'Selling Price'
            elif 'brand' in col_lower:
                column_mapping[col] = 'Brand'
            elif 'title' in col_lower or 'name' in col_lower or 'product' in col_lower:
                column_mapping[col] = 'Title'
            elif 'subcategory' in col_lower or 'sub' in col_lower:
                column_mapping[col] = 'Subcategory'
        
        df = df.rename(columns=column_mapping)
        
        # Check required columns
        required_columns = ['Image_URL', 'Brand', 'Title', 'Selling Price', 'Subcategory']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            st.info("Required columns: Image_URL, Brand, Title, Selling Price, Subcategory")
            return create_dummy_data()
        
        # Clean data
        df['Brand'] = df['Brand'].astype(str).str.strip()
        df['Title'] = df['Title'].astype(str).str.strip()
        df['Subcategory'] = df['Subcategory'].astype(str).str.strip()
        
        # Convert price to numeric
        df['Selling Price'] = pd.to_numeric(
            df['Selling Price'].astype(str)
            .str.replace('RM', '', regex=False)
            .str.replace('$', '', regex=False)
            .str.replace('€', '', regex=False)
            .str.replace('£', '', regex=False)
            .str.replace('₹', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip(), 
            errors='coerce'
        )
        
        # Remove rows with missing data
        df = df.dropna(subset=['Brand', 'Selling Price', 'Title', 'Subcategory'])
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return create_dummy_data()

def create_dummy_data():
    """Create dummy data for demonstration"""
    np.random.seed(42)
    
    data = {
        'Image_URL': [f'https://via.placeholder.com/300x400.png?text=Shoe+{i}' for i in range(50)],
        'Brand': np.random.choice(['London Rag', 'Rag & Co', 'Steve Madden', 'Aldo', 'Nine West', 'Call It Spring'], 50),
        'Title': np.random.choice([
            "Classic Ankle Boots", "Elegant Stiletto Heels", "Comfortable Ballet Flats",
            "Fashion Platform Sneakers", "Strappy Heeled Sandals", "Chelsea Leather Boots",
            "Block Heel Pumps", "Slip-On Loafers", "Knee-High Riding Boots",
            "Wedge Espadrilles", "Mary Jane Flats", "Athletic Running Sneakers"
        ], 50),
        'Selling Price': np.random.uniform(80, 300, 50).round(2),
        'Subcategory': np.random.choice([
            'Ankle Boots', 'Knee-High Boots', 'Pumps & Court Shoes', 'Stilettos', 
            'Ballet Flats', 'Loafers', 'Fashion Sneakers', 'Flat Sandals', 'Heeled Sandals'
        ], 50)
    }
    
    return pd.DataFrame(data)

# ========== ANALYSIS FUNCTIONS ==========
def calculate_metrics(df, brands):
    """Calculate key metrics for selected brands"""
    metrics = {}
    
    for brand in brands:
        brand_data = df[df['Brand'] == brand]
        metrics[brand] = {
            'avg_price': brand_data['Selling Price'].mean(),
            'min_price': brand_data['Selling Price'].min(),
            'max_price': brand_data['Selling Price'].max(),
            'total_products': len(brand_data)
        }
    
    return metrics

# ========== MAIN APP ==========
def main():
    # Set default currency
    currency = "₹"
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👠 Women's Shoes Competitive Analysis</h1>
        <p>Strategic pricing insights and product categorization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.image("https://via.placeholder.com/250x80.png?text=London+Rag", width='stretch')
        st.markdown("### 📊 Dashboard Controls")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Excel File", 
            type=['xlsx', 'xls'], 
            help="Upload your competitive data file with Subcategory column"
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
        
        st.success(f"✅ Loaded {len(df)} products")
        
        # Our Brands Filter
        st.markdown("### 🏷️ Our Brands")
        our_brand_options = ['London Rag', 'Rag & Co']
        available_our_brands = [b for b in our_brand_options if b in df['Brand'].unique()]
        
        selected_our_brands = st.multiselect(
            "Select Our Brands",
            available_our_brands,
            default=available_our_brands,
            help="Select one or both of our brands for analysis"
        )
        
        if not selected_our_brands:
            st.warning("⚠️ Please select at least one of our brands")
            return
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🔍 Filters")
        
        # Subcategory filter
        all_subcategories = ['All'] + sorted(df['Subcategory'].unique().tolist())
        selected_subcategory = st.selectbox("Subcategory", all_subcategories)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_subcategory != 'All':
            filtered_df = filtered_df[filtered_df['Subcategory'] == selected_subcategory]
        
        # Competitor brand selection
        all_brands = sorted(filtered_df['Brand'].unique().tolist())
        competitor_brands = [b for b in all_brands if b not in our_brand_options]
        
        # Default select top 3 competitors
        default_competitors = competitor_brands[:3] if len(competitor_brands) >= 3 else competitor_brands
        
        selected_competitors = st.multiselect(
            "Select Competitor Brands",
            competitor_brands,
            default=default_competitors,
            help="Select competitor brands for comparison"
        )
        
        # Combine all brands for filtering
        all_selected_brands = selected_our_brands + selected_competitors
        
        if not all_selected_brands:
            st.warning("⚠️ Please select at least one brand")
            return
        
        # Filter by all selected brands
        filtered_df = filtered_df[filtered_df['Brand'].isin(all_selected_brands)]
        
        st.markdown("---")
        st.markdown(f"**Filtered Results:** {len(filtered_df)} products")
    
    # ========== FILTER DISPLAY ==========
    filter_text = f"""
    <div class="filter-display">
        <h3>🔍 Active Filters</h3>
        <span class="filter-tag">🏷️ Our Brands: {', '.join(selected_our_brands)}</span>
        <span class="filter-tag">📌 Subcategory: {selected_subcategory}</span>
        <span class="filter-tag">⚔️ Competitors: {', '.join(selected_competitors) if selected_competitors else 'None'}</span>
    </div>
    """
    st.markdown(filter_text, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        return
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df, all_selected_brands)
    
    # ========== TABS ==========
    tab1, tab2, tab3 = st.tabs(["📊 Key Metrics", "📈 Charts & Analysis", "🖼️ Product Gallery"])
    
    # ========== TAB 1: KEY METRICS ==========
    with tab1:
        st.markdown("### 🎯 Performance Metrics")
        
        # Our Brands metrics
        st.markdown("#### 🏆 Our Brands Performance")
        
        # Display metrics for our brands side by side
        our_brand_cols = st.columns(len(selected_our_brands))
        
        for idx, our_brand in enumerate(selected_our_brands):
            if our_brand in metrics:
                with our_brand_cols[idx]:
                    st.markdown(f"**{our_brand}**")
                    brand_metrics = metrics[our_brand]
                    
                    st.metric(
                        "Avg Selling Price",
                        f"{currency} {brand_metrics['avg_price']:.2f}",
                        help="Average selling price across all products"
                    )
                    
                    st.metric(
                        "Price Range",
                        f"{currency} {brand_metrics['min_price']:.2f} - {currency} {brand_metrics['max_price']:.2f}",
                        help="Minimum to maximum price range"
                    )
                    
                    st.metric(
                        "Total Products",
                        brand_metrics['total_products'],
                        help="Number of products in dataset"
                    )
        
        # Competitor comparison
        if selected_competitors:
            st.markdown("---")
            st.markdown("#### ⚔️ Competitor Comparison")
            
            cols = st.columns(len(selected_competitors))
            for idx, brand in enumerate(selected_competitors):
                with cols[idx]:
                    st.markdown(f"**{brand}**")
                    st.metric("Avg Price", f"{currency} {metrics[brand]['avg_price']:.2f}")
                    st.metric("Price Range", f"{currency} {metrics[brand]['min_price']:.2f} - {currency} {metrics[brand]['max_price']:.2f}")
                    st.metric("Products", metrics[brand]['total_products'])
    
    # ========== TAB 2: CHARTS ==========
# ========== TAB 2: CHARTS ==========
    with tab2:
        st.markdown("### 📊 Visual Analysis")
        
        # Average Price Comparison
        st.markdown("#### Average Selling Price by Brand")
        price_data = pd.DataFrame([
            {'Brand': brand, 'Avg Price': metrics[brand]['avg_price'], 
             'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor'}
            for brand in all_selected_brands
        ]).sort_values('Avg Price', ascending=False)
        
        fig_price = px.bar(
            price_data, 
            x='Brand', 
            y='Avg Price',
            color='Type',
            color_discrete_map={'Our Brand': '#8b5cf6', 'Competitor': '#0ea5e9'},
            text=[f'{currency} {val:.2f}' for val in price_data['Avg Price']]
        )
        
        fig_price.update_traces(
            textposition='outside',
            textfont=dict(size=12, weight='bold'),
            marker_line=dict(width=2, color='darkblue')
        )
        
        fig_price.update_layout(
            height=450,
            xaxis_title="",
            yaxis_title=f"Average Price ({currency})",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=80, b=60, l=60, r=40),
            yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=False)
        )
        st.plotly_chart(fig_price, width='stretch', key="avg_price_chart")
        
        # Price Distribution Comparison
        st.markdown("---")
        st.markdown("#### 💎 Price Distribution by Brand")
        
        fig_box = go.Figure()
        
        for brand in all_selected_brands:
            brand_data = filtered_df[filtered_df['Brand'] == brand]
            is_our_brand = brand in selected_our_brands
            
            fig_box.add_trace(go.Box(
                y=brand_data['Selling Price'],
                name=brand,
                marker=dict(
                    color='rgb(139, 92, 246)' if is_our_brand else 'rgb(14, 165, 233)',
                    line=dict(width=2)
                ),
                boxmean='sd'
            ))
        
        fig_box.update_layout(
            height=450,
            xaxis_title="Brand",
            yaxis_title=f"Price Distribution ({currency})",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            showlegend=False,
            margin=dict(t=40, b=60, l=60, r=40),
            yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=False)
        )
        st.plotly_chart(fig_box, width='stretch', key="price_distribution_chart")
        
        # Price Extremes Table
        st.markdown("---")
        st.markdown("#### 💰 Highest & Lowest Priced Products by Brand")
        
        # Create table data
        price_extremes_data = []
        for brand in all_selected_brands:
            brand_data = filtered_df[filtered_df['Brand'] == brand]
            
            if len(brand_data) > 0:
                # Get max price product
                max_product = brand_data.loc[brand_data['Selling Price'].idxmax()]
                # Get min price product
                min_product = brand_data.loc[brand_data['Selling Price'].idxmin()]
                
                price_extremes_data.append({
                    'Brand': brand,
                    'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor',
                    'Price_Type': 'Highest',
                    'Product_Name': max_product['Title'],
                    'Price': max_product['Selling Price'],
                    'Image_URL': max_product['Image_URL'],
                    'Subcategory': max_product['Subcategory']
                })
                
                price_extremes_data.append({
                    'Brand': brand,
                    'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor',
                    'Price_Type': 'Lowest',
                    'Product_Name': min_product['Title'],
                    'Price': min_product['Selling Price'],
                    'Image_URL': min_product['Image_URL'],
                    'Subcategory': min_product['Subcategory']
                })
        
        # Display as organized columns
        for brand in all_selected_brands:
            brand_extremes = [item for item in price_extremes_data if item['Brand'] == brand]
            
            if brand_extremes:
                st.markdown(f"**{brand}** {'🏆' if brand in selected_our_brands else '⚔️'}")
                
                cols = st.columns([1, 3, 2, 2])
                
                with cols[0]:
                    st.markdown("**Image**")
                with cols[1]:
                    st.markdown("**Product Name**")
                with cols[2]:
                    st.markdown("**Subcategory**")
                with cols[3]:
                    st.markdown("**Price**")
                
                for item in brand_extremes:
                    cols = st.columns([1, 3, 2, 2])
                    
                    with cols[0]:
                        image_url = str(item['Image_URL']).strip()
                        if image_url and image_url != 'nan' and image_url.startswith(('http://', 'https://')):
                            try:
                                st.image(image_url, width=80)
                            except:
                                st.image("https://via.placeholder.com/80x80.png?text=N/A", width=80)
                        else:
                            st.image("https://via.placeholder.com/80x80.png?text=N/A", width=80)
                    
                    with cols[1]:
                        price_badge = "🔴 HIGH" if item['Price_Type'] == 'Highest' else "🟢 LOW"
                        st.markdown(f"{price_badge}")
                        st.markdown(f"<small>{item['Product_Name'][:50]}{'...' if len(item['Product_Name']) > 50 else ''}</small>", unsafe_allow_html=True)
                    
                    with cols[2]:
                        st.markdown(f"<small>{item['Subcategory']}</small>", unsafe_allow_html=True)
                    
                    with cols[3]:
                        st.markdown(f"**{currency} {item['Price']:.2f}**")
                
                st.markdown("---")
        
        st.markdown("<br>", unsafe_allow_html=True)
        

    
    # ========== TAB 3: PRODUCT GALLERY ==========
    with tab3:
        st.markdown("### 🖼️ Product Showcase")
        
        # Organize products by brand in columns
        if len(all_selected_brands) > 0:
            # Create columns for each brand
            brand_cols = st.columns(len(all_selected_brands))
            
            for idx, brand in enumerate(all_selected_brands):
                with brand_cols[idx]:
                    # Brand header
                    st.markdown(f"""
                    <div class="brand-column-header">
                        {brand}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get ALL products for this brand
                    brand_products = filtered_df[filtered_df['Brand'] == brand]
                    
                    if len(brand_products) > 0:
                        # Display all products in vertical layout
                        for _, product in brand_products.iterrows():
                            st.markdown('<div class="product-card">', unsafe_allow_html=True)
                            
                            # Better image handling with validation
                            image_url = str(product.get('Image_URL', '')).strip()
                            
                            # Check if image URL is valid
                            if image_url and image_url != 'nan' and image_url.startswith(('http://', 'https://')):
                                try:
                                    st.image(image_url, width='stretch')
                                except Exception as e:
                                    st.image("https://via.placeholder.com/300x400.png?text=Image+Unavailable", width='stretch')
                                    st.caption(f"⚠️ Image load error")
                            else:
                                st.image("https://via.placeholder.com/300x400.png?text=No+Image", width='stretch')
                            
                            st.markdown(f"<div class='product-brand'>{product['Brand']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-title'>{product['Title'][:60]}{'...' if len(product['Title']) > 60 else ''}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-price'>{currency} {product['Selling Price']:.2f}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-category'>Subcategory: {product['Subcategory']}</div>", unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info(f"No products available for {brand}")
        else:
            st.info("No products available for the selected filters.")

if __name__ == "__main__":
    main()
