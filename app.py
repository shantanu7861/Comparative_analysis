# ========== TAB 3: PRODUCT GALLERY ==========
    with tab3:
        st.markdown("### 🖼️ Product Gallery - Organized by Brand")
        
        if len(filtered_df) > 0:
            # Create columns for each brand (our brands first, then competitors)
            brand_order = selected_our_brands + selected_competitors
            brand_columns = st.columns(len(brand_order))
            
            for idx, brand in enumerate(brand_order):
                with brand_columns[idx]:
                    # Brand column header
                    is_our_brand = brand in selected_our_brands
                    header_color = 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)' if is_our_brand else 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)'
                    brand_emoji = '🏆' if is_our_brand else '⚔️'
                    
                    st.markdown(f"""
                    <div class="brand-column-header" style="background: {header_color};">
                        {brand_emoji} {brand}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get all products for this brand
                    brand_products = filtered_df[filtered_df['Brand'] == brand].sort_values('Selling Price')
                    
                    # Display each product
                    for _, product in brand_products.iterrows():
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)
                        
                        # Image handling with fallback
                        image_url = product.get('Image Link', '')
                        if pd.notna(image_url) and str(image_url).strip():
                            image_url = str(image_url).strip()
                            try:
                                st.markdown(f'<div class="product-image-container">', unsafe_allow_html=True)
                                st.image(image_url, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            except:
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%); 
                                            height: 200px; 
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
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%); 
                                        height: 200px; 
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
                        
                        # Subcategory badge
                        st.markdown(f"<div class='product-brand' style='color: #10b981;'>🏷️ {product['Subcategory']}</div>", unsafe_allow_html=True)
                        
                        # Product title
                        st.markdown(f"<div class='product-title'>{product['Title'][:60]}{'...' if len(product['Title']) > 60 else ''}</div>", unsafe_allow_html=True)
                        
                        # Price
                        st.markdown(f"<div class='product-price'>{currency} {product['Selling Price']:.2f}</div>", unsafe_allow_html=True)
                        
                        # Link
                        st.markdown(f"<a href='{product['Link']}' class='product-link' target='_blank'>View Product →</a>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No products available for the selected filters.")
