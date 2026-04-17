import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_universal_chart(df, chart_type, x, y=None, color=None, size=None, facet=None):
    """
    Elite Universal Rendering Engine.
    Fixes nested try-block syntax errors and missing constant definitions.
    """
    # 1. Configuration & Global Constants [cite: 335]
    THEME = "plotly_dark"
    COLOR_SCALE = px.colors.sequential.Viridis  # Fix: Defined missing scale
    DIVERGING_SCALE = px.colors.diverging.RdBu_r # Fix: Defined missing scale
    
    # FIX: Removed data_frame from opts to avoid 'multiple values' error 
    opts = {
        "template": THEME,
        "color_discrete_sequence": px.colors.qualitative.Prism,
    }

    # 2. Advanced Mapping Logic with Single Try Block 
    try:
        # Relationships & Multi-Dimensional Analysis [cite: 337]
        if chart_type == "Elite Scatter (4D)":
            fig = px.scatter(df, x=x, y=y, color=color, size=size, 
                             facet_col=facet if facet else None,
                             trendline="ols", hover_data=list(df.columns),
                             title=f"Multi-Dimensional Analysis: {x} vs {y}", **opts)

        elif chart_type == "Bubble Relationship":
            fig = px.scatter(df, x=x, y=y, size=size, color=color, 
                             log_x=True, size_max=60, title=f"Bubble Relationship of {x}", **opts)

        # Comparison & Ranking [cite: 12]
        elif chart_type == "Professional Bar":
            fig = px.bar(df, x=x, y=y, color=color, barmode="group",
                         text_auto='.2s', title=f"Comparison: {y} by {x}", **opts)
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        elif chart_type == "Tree Map (Hierarchical)":
            fig = px.treemap(df, path=[px.Constant("all"), color, x] if color else [x], 
                             values=y, color=y, color_continuous_scale=COLOR_SCALE,
                             title="Hierarchical Tree Map Distribution", **opts)

        # Statistical Distributions & Spreads [cite: 11, 209, 308]
        elif chart_type == "Advanced Violin":
            fig = px.violin(df, x=x, y=y, color=color, box=True, points="all",
                            hover_data=list(df.columns), title=f"Statistical Distribution: {y}", **opts)

        elif chart_type == "Box Spread (Outliers)":
            fig = px.box(df, x=x, y=y, color=color, notched=True, points="outliers",
                         title=f"Outlier Analysis for {y}", **opts)

        elif chart_type == "High-Density Histogram":
            fig = px.histogram(df, x=x, color=color, marginal="box", nbins=50,
                               title=f"Frequency Distribution: {x}", **opts)

        # Composition & Flow [cite: 13, 209, 309]
        elif chart_type == "Sunburst (Radial)":
            fig = px.sunburst(df, path=[color, x] if color else [x], values=y,
                              color=y, color_continuous_scale=COLOR_SCALE,
                              title="Radial Composition Analysis", **opts)

        elif chart_type == "Elite Pie":
            fig = px.pie(df, names=x, values=y, hole=0.5, 
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         title=f"Proportional Split: {x}", **opts)
            fig.update_traces(textposition='inside', textinfo='percent+label')

        # Trends & Temporal Data [cite: 13, 39, 59]
        elif chart_type == "Line (Time-Series)":
            fig = px.line(df, x=x, y=y, color=color, markers=True, 
                          line_shape="spline", render_mode="svg",
                          title=f"Trend Analysis: {y} Over Time", **opts)

        elif chart_type == "Area (Stacked)":
            fig = px.area(df, x=x, y=y, color=color, line_group=color,
                          title="Stacked Cumulative Growth", **opts)

        # Advanced Statistical/Correlation Matrix [cite: 310]
        elif chart_type == "Interactive Heatmap":
            corr = df.select_dtypes(include=[np.number]).corr()
            fig = px.imshow(corr, text_auto='.2f', aspect="auto",
                            color_continuous_scale=DIVERGING_SCALE,
                            title="Interactive Feature Correlation Matrix", **opts)

        elif chart_type == "Density Heatmap":
            fig = px.density_heatmap(df, x=x, y=y, z=y, nbinsx=30, nbinsy=30,
                                     color_continuous_scale=COLOR_SCALE,
                                     title="Data Density/Concentration Map", **opts)

        # Polar & Specialized [cite: 310]
        elif chart_type == "Spider/Radar Chart":
            fig = px.line_polar(df, r=y, theta=x, color=color, line_close=True,
                                markers=True, title="Spider/Radar Multi-Attribute Analysis", **opts)
            fig.update_traces(fill='toself')

        elif chart_type == "Parallel Categories":
            fig = px.parallel_categories(df, dimensions=[x] if not color else [color, x],
                                         color=y, color_continuous_scale=COLOR_SCALE,
                                         title="Multi-Stage Flow Analysis", **opts)

        else:
            return None

        # 3. Global Layout Optimization [cite: 338, 339]
        fig.update_layout(
            font_family="Inter, sans-serif",
            title_font_size=24,
            legend_title_font_color="white",
            paper_bgcolor='rgba(0,0,0,0)',  # Glassmorphism support [cite: 298, 335]
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20),
            hoverlabel=dict(bgcolor="black", font_size=13, font_family="Inter"),
        )
        
        # Grid aesthetics [cite: 338]
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.1)')
        
        return fig

    except Exception as e:
        # Professional fail-safe for universal data handling 
        return go.Figure().add_annotation(text=f"Configuration Error: {str(e)}", 
                                          showarrow=False, font_size=20)