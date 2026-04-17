import pandas as pd
import numpy as np
from scipy import stats

def get_detailed_profile(df):
    """
    World-class exhaustive profiler. 
    Handles deep statistical audits including skewness, kurtosis, and outlier detection.
    """
    profile = {
        "shape": df.shape,
        "total_nulls": int(df.isnull().sum().sum()),
        "total_cells": int(df.size),
        "null_percentage": f"{(df.isnull().sum().sum() / df.size) * 100:.2f}%",
        "duplicates": int(df.duplicated().sum()),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
        "columns": {}
    }
    
    for col in df.columns:
        col_data = df[col]
        is_num = pd.api.types.is_numeric_dtype(col_data)
        
        # Base stats for every column type
        stats_dict = {
            "dtype": str(col_data.dtype),
            "uniques": col_data.nunique(),
            "completeness": f"{(1 - col_data.isnull().mean()) * 100:.1f}%",
            "is_numeric": is_num
        }

        # Deep Statistical Audit for Numerical Columns
        if is_num and not col_data.empty:
            clean_col = col_data.dropna()
            if not clean_col.empty:
                # Distribution & Spread
                stats_dict.update({
                    "mean": float(clean_col.mean()),
                    "median": float(clean_col.median()),
                    "std": float(clean_col.std()),
                    "min": float(clean_col.min()),
                    "max": float(clean_col.max()),
                    "skew": float(clean_col.skew()),
                    "kurtosis": float(clean_col.kurtosis()),
                })
                
                # Professional Outlier Detection (Z-Score method)
                z_scores = np.abs(stats.zscore(clean_col))
                outliers = np.where(z_scores > 3)[0]
                stats_dict["outlier_count"] = len(outliers)
        
        # Frequency Audit for Categorical Columns
        else:
            stats_dict["top_value"] = str(col_data.mode()[0]) if not col_data.mode().empty else "N/A"
            stats_dict["value_counts"] = col_data.value_counts().head(5).to_dict()

        profile["columns"][col] = stats_dict
        
    return profile

def smart_cleaner(df, action, target_col=None):
    """
    Advanced Self-Correction Engine.
    Supports targeted cleaning and global strategies for a professional workflow.
    """
    df_clean = df.copy()

    if action == "Drop All Nulls":
        return df_clean.dropna().reset_index(drop=True)

    if action == "Drop Duplicate Rows":
        return df_clean.drop_duplicates().reset_index(drop=True)

    if action == "Remove Outliers (Z-Score)":
        num_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            z_scores = np.abs(stats.zscore(df_clean[col].fillna(df_clean[col].median())))
            df_clean = df_clean[z_scores < 3]
        return df_clean.reset_index(drop=True)

    if action == "Deep Fill Strategy":
        for col in df_clean.columns:
            # Numerical: Use Median for skewed data, Mean for normal
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                if abs(df_clean[col].skew()) > 1:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                else:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            # Categorical: Use Mode (Most Frequent)
            else:
                if not df_clean[col].mode().empty:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        return df_clean

    if action == "Normalize Data (Scaling)":
        num_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            min_val = df_clean[col].min()
            max_val = df_clean[col].max()
            if max_val != min_val:
                df_clean[col] = (df_clean[col] - min_val) / (max_val - min_val)
        return df_clean

    return df_clean