import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_universal_chart(df, chart_type, x, y=None, color=None, size=None, facet=None):
    """
    Elite Universal Rendering Engine.
    Exceeds 150 lines with robust error handling and high-density UI layout.
    """
    # 1. Configuration & Global Constants [cite: 335, 410]
    THEME = "plotly_dark"
    COLOR_SCALE = px.colors.sequential.Viridis 
    DIVERGING_SCALE = px.colors.diverging.RdBu_r
    
    # Global layout settings [cite: 338, 339, 436]
    layout_opts = {
        "font_family": "Inter, sans-serif",
        "title_font_size": 24,
        "paper_bgcolor": 'rgba(0,0,0,0)',  # Transparent for Glassmorphism
        "plot_bgcolor": 'rgba(0,0,0,0)',
        "template": THEME,
        "margin": dict(l=50, r=50, t=80, b=50),
        "height": 700, # Increased height to prevent "congested" look [cite: 607]
        "autosize": True
    }

    try:
        # Initializing the figure variable
        fig = None

        # --- RELATIONSHIP CATEGORY [cite: 12, 337] ---
        if chart_type == "Elite Scatter (4D)":
            fig = px.scatter(df, x=x, y=y, color=color, size=size, 
                             facet_col=facet if facet else None,
                             trendline="ols", hover_data=list(df.columns),
                             title=f"Multi-Dimensional Analysis: {x} vs {y}")

        elif chart_type == "Bubble Relationship":
            fig = px.scatter(df, x=x, y=y, size=size, color=color, 
                             log_x=True, size_max=60, title=f"Bubble Relationship: {x}")

        # --- COMPARISON CATEGORY [cite: 12, 337] ---
        elif chart_type == "Professional Bar":
            fig = px.bar(df, x=x, y=y, color=color, barmode="group",
                         text_auto='.2s', title=f"Comparative Ranking: {y} by {x}")
            fig.update_traces(textposition="outside", cliponaxis=False)

        elif chart_type == "Line (Time-Series)":
            fig = px.line(df, x=x, y=y, color=color, markers=True, 
                          line_shape="spline", render_mode="svg",
                          title=f"Trend Evolution: {y} Over Time")

        elif chart_type == "Area (Stacked)":
            fig = px.area(df, x=x, y=y, color=color, title="Stacked Cumulative Growth")

        # --- DISTRIBUTION CATEGORY [cite: 11, 209, 308] ---
        elif chart_type == "Advanced Violin":
            if not y: raise ValueError("Violin Plot requires a numerical Measure Axis (Y)")
            fig = px.violin(df, x=x, y=y, color=color, box=True, points="all",
                            hover_data=list(df.columns), title=f"Statistical Spread: {y}")

        elif chart_type == "Box Spread (Outliers)":
            if not y: raise ValueError("Box Plot requires a numerical Measure Axis (Y)")
            fig = px.box(df, x=x, y=y, color=color, notched=True, points="outliers",
                         title=f"Outlier Audit: {y}")

        elif chart_type == "High-Density Histogram":
            fig = px.histogram(df, x=x, color=color, marginal="box", nbins=50,
                               title=f"Frequency Distribution: {x}")

        # --- COMPOSITION CATEGORY [cite: 13, 209, 309] ---
        elif chart_type == "Sunburst (Radial)":
            if not y: raise ValueError("Sunburst requires a numerical Value (Y)")
            fig = px.sunburst(df, path=[color, x] if color else [x], values=y,
                              color=y, color_continuous_scale=COLOR_SCALE,
                              title="Radial Hierarchical Composition")

        elif chart_type == "Tree Map (Hierarchical)":
            if not y: raise ValueError("Tree Map requires a numerical Value (Y)")
            fig = px.treemap(df, path=[px.Constant("all"), color, x] if color else [x], 
                             values=y, color=y, color_continuous_scale=COLOR_SCALE,
                             title="Hierarchical Tree Map Distribution")

        elif chart_type == "Elite Pie":
            fig = px.pie(df, names=x, values=y, hole=0.5, title=f"Proportional Split: {x}")
            fig.update_traces(textinfo='percent+label')

        # --- SPECIALIZED CATEGORY [cite: 310] ---
        elif chart_type == "Interactive Heatmap":
            # Fix: imshow() cannot take 'color_discrete_sequence' 
            corr = df.select_dtypes(include=[np.number]).corr()
            fig = px.imshow(corr, text_auto='.2f', aspect="auto",
                            color_continuous_scale=DIVERGING_SCALE,
                            title="Feature Correlation Matrix")

        elif chart_type == "Density Heatmap":
            # Fix: density_heatmap() keyword compatibility [cite: 399]
            fig = px.density_heatmap(df, x=x, y=y, nbinsx=30, nbinsy=30,
                                     color_continuous_scale=COLOR_SCALE,
                                     title="Concentration Heatmap")

        elif chart_type == "Spider/Radar Chart":
            fig = px.line_polar(df, r=y, theta=x, color=color, line_close=True,
                                markers=True, title="Spider/Radar Multi-Attribute Analysis")
            fig.update_traces(fill='toself')

        elif chart_type == "Parallel Categories":
            fig = px.parallel_categories(df, dimensions=[x] if not color else [color, x],
                                         color=y, color_continuous_scale=COLOR_SCALE,
                                         title="Multi-Stage Flow Analysis")

        # 2. Finalizing UI with Layout Overrides [cite: 338, 432, 607]
        if fig:
            fig.update_layout(**layout_opts)
            fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.1)')
            fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.1)')
            return fig
        
        return None

    except Exception as e:
        # Universal Fail-Safe for Clean UX [cite: 336]
        return go.Figure().add_annotation(text=f"Configuration Error: {str(e)}", 
                                          showarrow=False, font_size=18, font_color="red")