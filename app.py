import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import openai
from openai import OpenAI
from datetime import datetime

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
    
    /* Insight box styling */
    .insight-box {
        background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 12px;
        margin-top: 1.2rem;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .insight-box h3 {
        margin-top: 0;
        font-size: 1.5rem;
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
            # Try to load default file
            default_path = Path("data.xlsx")
            if default_path.exists():
                df = pd.read_excel(default_path, sheet_name="Sheet1")
            else:
                # Create dummy data for demonstration
                return create_dummy_data()
        else:
            df = pd.read_excel(file_path, sheet_name="Sheet1")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert price column to numeric
        df['Selling Price'] = pd.to_numeric(df['Selling Price'].astype(str).str.replace('RM', '').str.replace(',', '').str.strip(), errors='coerce')
        
        # Clean text columns
        df['Brand'] = df['Brand'].astype(str).str.strip()
        df['Category'] = df['Category'].astype(str).str.strip()
        df['Market place'] = df['Market place'].astype(str).str.strip()
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['Brand', 'Selling Price'])
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return create_dummy_data()

def create_dummy_data():
    """Create dummy data for demonstration"""
    np.random.seed(42)
    brands = ['London Rag', 'Rag & Co', 'Steve Madden', 'Aldo', 'Nine West', 'Call It Spring']
    categories = ['Mary Jane', 'Loafer', 'Boot', 'Heels', 'Sandals']
    marketplaces = ['Zalora', "Macy's", 'Namshi', 'Amazon']
    
    n_products = 60
    data = {
        'Link': [f'https://example.com/product_{i}' for i in range(n_products)],
        'Image Link': [f'https://via.placeholder.com/300x400.png?text=Product+{i}' for i in range(n_products)],
        'Brand': np.random.choice(brands, n_products),
        'Title': [f'Stylish {np.random.choice(categories)} - Style {i}' for i in range(n_products)],
        'Selling Price': np.random.uniform(150, 350, n_products).round(2),
        'Category': np.random.choice(categories, n_products),
        'Market place': np.random.choice(marketplaces, n_products)
    }
    
    df = pd.DataFrame(data)
    
    return df

# ========== ANALYSIS FUNCTIONS ==========
def calculate_metrics(df, brands):
    """Calculate key metrics for selected brands"""
    metrics = {}
    
    for brand in brands:
        brand_data = df[df['Brand'] == brand]
        metrics[brand] = {
            'avg_price': brand_data['Selling Price'].mean(),
            'total_products': len(brand_data)
        }
    
    return metrics

def calculate_individual_price_gaps(metrics, our_brands, competitor_brands, currency):
    """Calculate price gap between our brands and each competitor"""
    price_gaps = []
    
    for our_brand in our_brands:
        if our_brand not in metrics:
            continue
        
        our_price = metrics[our_brand]['avg_price']
        
        # Compare with all competitors
        for comp_brand in competitor_brands:
            if comp_brand in metrics:
                competitor_price = metrics[comp_brand]['avg_price']
                if competitor_price > 0:
                    gap = ((competitor_price - our_price) / competitor_price * 100).round(2)
                    price_gaps.append({
                        'Our Brand': our_brand,
                        f'Our Avg Price': our_price,
                        'Competitor': comp_brand,
                        f'Competitor Avg Price': competitor_price,
                        'Price Gap %': gap
                    })
        
        # Also compare with other "our brands" if multiple selected
        for other_our_brand in our_brands:
            if other_our_brand != our_brand and other_our_brand in metrics:
                other_price = metrics[other_our_brand]['avg_price']
                if other_price > 0:
                    gap = ((other_price - our_price) / other_price * 100).round(2)
                    price_gaps.append({
                        'Our Brand': our_brand,
                        f'Our Avg Price': our_price,
                        'Competitor': f"{other_our_brand} (Our Brand)",
                        f'Competitor Avg Price': other_price,
                        'Price Gap %': gap
                    })
    
    return pd.DataFrame(price_gaps)

def generate_ai_insights(df, metrics, our_brands, competitor_brands, selected_category, selected_marketplace, api_key, currency):
    """Generate AI-powered insights using OpenAI GPT-4o-mini"""
    if not api_key:
        return ["Please provide an OpenAI API key to generate AI-powered insights."]
    
    try:
        client = OpenAI(api_key=api_key)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Prepare data summary for AI
        data_summary = f"""
        Today's date: {current_date}
        
        Analyze this competitive pricing data for our fashion brands:
        
        OUR BRANDS: {', '.join(our_brands)}
        """
        
        for brand in our_brands:
            if brand in metrics:
                data_summary += f"""
        
        {brand} Metrics:
        - Average Selling Price: {currency} {metrics[brand]['avg_price']:.2f}
        - Total Products: {metrics[brand]['total_products']}
        """
        
        data_summary += f"""
        
        COMPETITORS: {', '.join(competitor_brands)}
        """
        
        for brand in competitor_brands:
            if brand in metrics:
                data_summary += f"""
        {brand}:
          - Avg Price: {currency} {metrics[brand]['avg_price']:.2f}
          - Products: {metrics[brand]['total_products']}
        """
        
        # Add filter context
        data_summary += f"""
        
        Current Analysis Filters:
        - Category: {selected_category}
        - Marketplace: {selected_marketplace}
        """
        
        # Category distribution
        if 'Category' in df.columns:
            for our_brand in our_brands:
                if our_brand in df['Brand'].values:
                    brand_data = df[df['Brand'] == our_brand]
                    data_summary += f"\n\nCategory Distribution for {our_brand}:\n"
                    cat_counts = brand_data['Category'].value_counts().head(3)
                    for cat, count in cat_counts.items():
                        data_summary += f"  - {cat}: {count} products\n"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are an expert fashion retail pricing strategist. Today is {current_date}. 

Provide 5-6 highly actionable pricing and strategic insights based on the competitive data. Focus on:

1. **Pricing Strategy**: Should we increase/decrease prices? By how much? Why?
2. **Market Positioning**: How do our prices position us in the market (value/mid-range/premium)?
3. **Category Opportunities**: Which categories should we focus on based on pricing gaps?
4. **Competitive Analysis**: How do we compare to specific competitors?
5. **Immediate Actions**: What specific actions should be taken this week/month?
6. **Seasonal Recommendations**: Given the current date, suggest relevant seasonal pricing strategies

Each insight should be:
- Specific with numbers and percentages
- Actionable with clear recommendations
- Business-focused (revenue, margins, market share)
- Consider current market conditions and timing
- Use emojis for visual appeal

Format: Start each insight with an emoji and bold title, followed by 2-3 sentences with specific recommendations."""},
                {"role": "user", "content": data_summary}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        ai_insights = response.choices[0].message.content.strip().split('\n\n')
        return [insight.strip() for insight in ai_insights if insight.strip()]
    
    except Exception as e:
        st.warning(f"AI insights unavailable: {str(e)}")
        return [f"⚠️ Unable to generate AI insights. Error: {str(e)}"]

# ========== MAIN APP ==========
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👠 Competitive Analysis Dashboard</h1>
        <p>Data-driven insights for strategic pricing and market positioning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.image("https://via.placeholder.com/250x80.png?text=London+Rag", use_container_width=True)
        st.markdown("### 📊 Dashboard Controls")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'], help="Upload your competitive data file")
        
        st.markdown("---")
        
        # Currency selector
        st.markdown("### 💱 Currency")
        currency = st.selectbox("Select Currency", ["RM", "$", "€", "£", "₹"], index=0)
        
        st.markdown("---")
        
        # OpenAI API Key input
        st.markdown("### 🤖 AI Insights")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key for AI-powered pricing insights",
            placeholder="sk-..."
        )
        
        if api_key:
            st.success("✅ AI insights enabled")
        else:
            st.info("ℹ️ Add API key for AI insights")
        
        st.markdown("---")
        
        # Load data
        if uploaded_file is not None:
            df = load_data(uploaded_file)
        else:
            df = load_data()
        
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
        
        # Category filter
        all_categories = ['All'] + sorted(df['Category'].unique().tolist())
        selected_category = st.selectbox("Category", all_categories)
        
        # Marketplace filter
        all_marketplaces = ['All'] + sorted(df['Market place'].unique().tolist())
        selected_marketplace = st.selectbox("Marketplace", all_marketplaces)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        if selected_marketplace != 'All':
            filtered_df = filtered_df[filtered_df['Market place'] == selected_marketplace]
        
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
    st.markdown(f"""
    <div class="filter-display">
        <h3>🔍 Active Filters</h3>
        <span class="filter-tag">💱 Currency: {currency}</span>
        <span class="filter-tag">🏷️ Our Brands: {', '.join(selected_our_brands)}</span>
        <span class="filter-tag">📂 Category: {selected_category}</span>
        <span class="filter-tag">🏪 Marketplace: {selected_marketplace}</span>
        <span class="filter-tag">⚔️ Competitors: {', '.join(selected_competitors) if selected_competitors else 'None'}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    if len(filtered_df) == 0:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        return
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df, all_selected_brands)
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Key Metrics", "📈 Charts & Analysis", "🖼️ Product Gallery", "💡 Strategic Insights"])
    
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
                    st.metric("Products", metrics[brand]['total_products'])
        
        # Price gap breakdown
        st.markdown("---")
        st.markdown("#### 💰 Price Gap Breakdown by Competitor")
        price_gap_df = calculate_individual_price_gaps(metrics, selected_our_brands, selected_competitors + [b for b in selected_our_brands], currency)
        
        if not price_gap_df.empty:
            st.dataframe(
                price_gap_df.style.format({
                    'Our Avg Price': f'{currency} {{:.2f}}',
                    'Competitor Avg Price': f'{currency} {{:.2f}}',
                    'Price Gap %': '{:.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Select competitor brands to see price gap breakdown")
    
    # ========== TAB 2: CHARTS ==========
    with tab2:
        st.markdown("### 📊 Visual Analysis")
        
        # Chart 1: Average Price Comparison
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### Average Selling Price by Brand")
            price_data = pd.DataFrame([
                {'Brand': brand, 'Avg Price': metrics[brand]['avg_price'], 
                 'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor'}
                for brand in all_selected_brands
            ]).sort_values('Avg Price', ascending=False)
            
            fig_price = go.Figure()
            
            # Our brands
            our_brand_data = price_data[price_data['Type'] == 'Our Brand']
            fig_price.add_trace(go.Bar(
                x=our_brand_data['Brand'],
                y=our_brand_data['Avg Price'],
                name='Our Brands',
                marker=dict(
                    color=our_brand_data['Avg Price'],
                    colorscale='Purples',
                    showscale=False,
                    line=dict(color='rgb(99, 102, 241)', width=2)
                ),
                text=[f'{currency} {val:.2f}' for val in our_brand_data['Avg Price']],
                textposition='outside',
                textfont=dict(size=12, weight='bold')
            ))
            
            # Competitors
            comp_data = price_data[price_data['Type'] == 'Competitor']
            fig_price.add_trace(go.Bar(
                x=comp_data['Brand'],
                y=comp_data['Avg Price'],
                name='Competitors',
                marker=dict(
                    color=comp_data['Avg Price'],
                    colorscale='Blues',
                    showscale=False,
                    line=dict(color='rgb(14, 165, 233)', width=2)
                ),
                text=[f'{currency} {val:.2f}' for val in comp_data['Avg Price']],
                textposition='outside',
                textfont=dict(size=12, weight='bold')
            ))
            
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
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=False),
                xaxis=dict(categoryorder='array', categoryarray=price_data['Brand'].tolist())
            )
            st.plotly_chart(fig_price, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### Product Count by Brand")
            product_data = pd.DataFrame([
                {'Brand': brand, 'Product Count': metrics[brand]['total_products'],
                 'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor'}
                for brand in all_selected_brands
            ]).sort_values('Product Count', ascending=False)
            
            fig_products = go.Figure()
            
            # Our brands
            our_brand_prod = product_data[product_data['Type'] == 'Our Brand']
            fig_products.add_trace(go.Bar(
                x=our_brand_prod['Brand'],
                y=our_brand_prod['Product Count'],
                name='Our Brands',
                marker=dict(
                    color=our_brand_prod['Product Count'],
                    colorscale='Pinkyl',
                    showscale=False,
                    line=dict(color='rgb(236, 72, 153)', width=2)
                ),
                text=[f'{val}' for val in our_brand_prod['Product Count']],
                textposition='outside',
                textfont=dict(size=12, weight='bold')
            ))
            
            # Competitors
            comp_prod = product_data[product_data['Type'] == 'Competitor']
            fig_products.add_trace(go.Bar(
                x=comp_prod['Brand'],
                y=comp_prod['Product Count'],
                name='Competitors',
                marker=dict(
                    color=comp_prod['Product Count'],
                    colorscale='Teal',
                    showscale=False,
                    line=dict(color='rgb(6, 182, 212)', width=2)
                ),
                text=[f'{val}' for val in comp_prod['Product Count']],
                textposition='outside',
                textfont=dict(size=12, weight='bold')
            ))
            
            fig_products.update_layout(
                height=450,
                xaxis_title="",
                yaxis_title="Product Count",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=80, b=60, l=60, r=40),
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zeroline=False),
                xaxis=dict(categoryorder='array', categoryarray=product_data['Brand'].tolist())
            )
            st.plotly_chart(fig_products, use_container_width=True)
        
        # Price Distribution Comparison
        st.markdown("---")
        st.markdown("#### 💎 Price Distribution Comparison")
        
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
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Price Statistics
        st.markdown("---")
        st.markdown("#### 📋 Price Statistics")
        stats_df = pd.DataFrame([
            {
                'Brand': brand,
                'Type': 'Our Brand' if brand in selected_our_brands else 'Competitor',
                'Min Price': filtered_df[filtered_df['Brand'] == brand]['Selling Price'].min(),
                'Max Price': filtered_df[filtered_df['Brand'] == brand]['Selling Price'].max(),
                'Avg Price': metrics[brand]['avg_price'],
                'Products': metrics[brand]['total_products']
            }
            for brand in all_selected_brands
        ])
        st.dataframe(stats_df.style.format({
            'Min Price': f'{currency} {{:.2f}}',
            'Max Price': f'{currency} {{:.2f}}',
            'Avg Price': f'{currency} {{:.2f}}'
        }), use_container_width=True, hide_index=True)
    
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
                            
                            # Image handling with fallback
                            image_url = product.get('Image Link', '')
                            if pd.notna(image_url) and str(image_url).strip():
                                # Clean the URL
                                image_url = str(image_url).strip()
                                
                                # Try to display the image
                                try:
                                    st.image(image_url, use_container_width=True)
                                except Exception as e:
                                    # If image fails, show placeholder with product info
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%); 
                                                height: 220px; 
                                                border-radius: 10px; 
                                                display: flex; 
                                                align-items: center; 
                                                justify-content: center;
                                                margin-bottom: 0.8rem;
                                                color: #6366f1;
                                                font-weight: 600;
                                                text-align: center;
                                                padding: 1rem;">
                                        📷<br>Image unavailable
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                # No image URL provided
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%); 
                                            height: 220px; 
                                            border-radius: 10px; 
                                            display: flex; 
                                            align-items: center; 
                                            justify-content: center;
                                            margin-bottom: 0.8rem;
                                            color: #6366f1;
                                            font-weight: 600;
                                            text-align: center;
                                            padding: 1rem;">
                                    📷<br>No image
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown(f"<div class='product-brand'>{product['Brand']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-title'>{product['Title'][:60]}{'...' if len(product['Title']) > 60 else ''}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='product-price'>{currency} {product['Selling Price']:.2f}</div>", unsafe_allow_html=True)
                            
                            st.markdown(f"<a href='{product['Link']}' class='product-link' target='_blank'>View Product →</a>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info(f"No products available for {brand}")
        else:
            st.info("No products available for the selected filters.")
    
    # ========== TAB 4: INSIGHTS ==========
    with tab4:
        st.markdown("### 💡 Strategic Insights & Recommendations")
        
        with st.spinner("Generating AI-powered pricing insights..."):
            insights = generate_ai_insights(
                filtered_df, 
                metrics, 
                selected_our_brands, 
                selected_competitors,
                selected_category,
                selected_marketplace,
                api_key,
                currency
            )
        
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                {insight}
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
