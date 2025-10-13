import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataCleaningPipeline:
    def __init__(self):
        self.scalers = {}
        self.cleaning_params = {}
        
    def detect_missing_values(self, df, threshold=0.5):
        """
        Detect missing values and return summary
        """
        missing_summary = {
            'total_missing': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'columns_with_missing': df.isnull().sum()[df.isnull().sum() > 0].to_dict(),
            'columns_missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
        }
        
        # Identify columns with high missing percentage
        high_missing_cols = [col for col in df.columns 
                           if (df[col].isnull().sum() / len(df)) > threshold]
        
        missing_summary['high_missing_columns'] = high_missing_cols
        
        return missing_summary
    
    def handle_missing_values(self, df, strategy='auto', numeric_strategy='mean', 
                            categorical_strategy='mode', drop_threshold=0.7):
        """
        Handle missing values based on specified strategy
        """
        df_clean = df.copy()
        
        # Auto strategy: determine based on data type and missing percentage
        if strategy == 'auto':
            for column in df_clean.columns:
                missing_ratio = df_clean[column].isnull().sum() / len(df_clean)
                
                # Drop columns with too many missing values
                if missing_ratio > drop_threshold:
                    df_clean = df_clean.drop(columns=[column])
                    continue
                
                # Handle based on data type
                if pd.api.types.is_numeric_dtype(df_clean[column]):
                    if missing_ratio > 0.3:
                        # Use median for skewed distributions
                        df_clean[column].fillna(df_clean[column].median(), inplace=True)
                    else:
                        df_clean[column].fillna(df_clean[column].mean(), inplace=True)
                else:
                    df_clean[column].fillna(df_clean[column].mode()[0] 
                                          if not df_clean[column].mode().empty 
                                          else 'Unknown', inplace=True)
        
        # Manual strategy
        else:
            for column in df_clean.columns:
                if df_clean[column].isnull().any():
                    if pd.api.types.is_numeric_dtype(df_clean[column]):
                        if numeric_strategy == 'mean':
                            df_clean[column].fillna(df_clean[column].mean(), inplace=True)
                        elif numeric_strategy == 'median':
                            df_clean[column].fillna(df_clean[column].median(), inplace=True)
                        elif numeric_strategy == 'mode':
                            df_clean[column].fillna(df_clean[column].mode()[0], inplace=True)
                        elif numeric_strategy == 'drop':
                            df_clean = df_clean.dropna(subset=[column])
                    else:
                        if categorical_strategy == 'mode':
                            df_clean[column].fillna(df_clean[column].mode()[0] 
                                                  if not df_clean[column].mode().empty 
                                                  else 'Unknown', inplace=True)
                        elif categorical_strategy == 'unknown':
                            df_clean[column].fillna('Unknown', inplace=True)
                        elif categorical_strategy == 'drop':
                            df_clean = df_clean.dropna(subset=[column])
        
        self.cleaning_params['missing_values_handled'] = True
        return df_clean
    
    def detect_outliers(self, df, method='iqr', threshold=3):
        """
        Detect outliers using different methods
        """
        outliers_summary = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = df[column].dropna()
            
            if method == 'iqr':
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(col_data))
                outliers = col_data[z_scores > threshold]
            
            elif method == 'modified_zscore':
                median = np.median(col_data)
                mad = np.median(np.abs(col_data - median))
                modified_z_scores = 0.6745 * (col_data - median) / mad
                outliers = col_data[np.abs(modified_z_scores) > threshold]
            
            outliers_summary[column] = {
                'outlier_count': len(outliers),
                'outlier_percentage': (len(outliers) / len(col_data)) * 100,
                'outlier_values': outliers.tolist()
            }
        
        return outliers_summary
    
    def handle_outliers(self, df, method='cap', **kwargs):
        """
        Handle outliers using different methods
        """
        df_clean = df.copy()
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            if method == 'cap':
                # Cap outliers at specified percentiles
                lower_percentile = kwargs.get('lower_percentile', 1)
                upper_percentile = kwargs.get('upper_percentile', 99)
                
                lower_bound = df_clean[column].quantile(lower_percentile / 100)
                upper_bound = df_clean[column].quantile(upper_percentile / 100)
                
                df_clean[column] = np.where(df_clean[column] < lower_bound, lower_bound, 
                                          np.where(df_clean[column] > upper_bound, upper_bound, 
                                                  df_clean[column]))
            
            elif method == 'remove':
                # Remove outliers using IQR
                Q1 = df_clean[column].quantile(0.25)
                Q3 = df_clean[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_clean = df_clean[(df_clean[column] >= lower_bound) & 
                                  (df_clean[column] <= upper_bound)]
            
            elif method == 'transform':
                # Apply log transformation
                if (df_clean[column] > 0).all():
                    df_clean[column] = np.log1p(df_clean[column])
        
        self.cleaning_params['outliers_handled'] = True
        return df_clean
    
    def normalize_data(self, df, method='standard', columns=None):
        """
        Normalize data using different scaling methods
        """
        df_normalized = df.copy()
        
        if columns is None:
            columns = df_normalized.select_dtypes(include=[np.number]).columns
        
        for column in columns:
            if column not in self.scalers:
                if method == 'standard':
                    self.scalers[column] = StandardScaler()
                elif method == 'minmax':
                    self.scalers[column] = MinMaxScaler()
                elif method == 'robust':
                    self.scalers[column] = RobustScaler()
            
            # Reshape for scaler and handle missing values temporarily
            col_data = df_normalized[column].values.reshape(-1, 1)
            mask = ~np.isnan(col_data).flatten()
            
            if mask.any():
                self.scalers[column].fit(col_data[mask])
                df_normalized[column] = self.scalers[column].transform(col_data).flatten()
        
        self.cleaning_params['normalization_method'] = method
        return df_normalized
    
    def create_cleaning_report(self, original_df, cleaned_df):
        """
        Create a comprehensive cleaning report
        """
        report = {
            'original_shape': original_df.shape,
            'cleaned_shape': cleaned_df.shape,
            'rows_removed': original_df.shape[0] - cleaned_df.shape[0],
            'columns_removed': original_df.shape[1] - cleaned_df.shape[1],
            'original_missing_values': original_df.isnull().sum().sum(),
            'cleaned_missing_values': cleaned_df.isnull().sum().sum(),
            'data_types': cleaned_df.dtypes.to_dict(),
            'cleaning_parameters': self.cleaning_params
        }
        
        return report
    
    def run_full_pipeline(self, df, missing_strategy='auto', outlier_method='cap', 
                         normalization_method='standard'):
        """
        Run the complete data cleaning pipeline
        """
        print("Starting data cleaning pipeline...")
        
        # Step 1: Analyze missing values
        print("1. Analyzing missing values...")
        missing_report = self.detect_missing_values(df)
        print(f"   Found {missing_report['total_missing']} missing values")
        
        # Step 2: Handle missing values
        print("2. Handling missing values...")
        df_clean = self.handle_missing_values(df, strategy=missing_strategy)
        
        # Step 3: Detect outliers
        print("3. Detecting outliers...")
        outlier_report = self.detect_outliers(df_clean)
        total_outliers = sum([report['outlier_count'] for report in outlier_report.values()])
        print(f"   Found {total_outliers} outliers")
        
        # Step 4: Handle outliers
        print("4. Handling outliers...")
        df_clean = self.handle_outliers(df_clean, method=outlier_method)
        
        # Step 5: Normalize data
        print("5. Normalizing data...")
        df_clean = self.normalize_data(df_clean, method=normalization_method)
        
        # Step 6: Generate report
        print("6. Generating cleaning report...")
        report = self.create_cleaning_report(df, df_clean)
        
        print("Data cleaning pipeline completed successfully!")
        return df_clean, report
