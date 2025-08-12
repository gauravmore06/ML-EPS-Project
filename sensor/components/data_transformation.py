from sqlite3 import SQLITE_DBCONFIG_LEGACY_ALTER_TABLE
import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
import sensor
import sensor.ml
import sensor.ml.model
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, robust_scale
from sklearn.pipeline import Pipeline

from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class DataTransformation:

    def __init__ (self, data_validation_artifact:DataValidationArtifact, Data_transfornation_config:DataTransformationConfig):
        """
        data_validation_artifact = Output referance of data ingestion artifact stage
        Data_transfornation_config = config for data Transformation
        
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = Data_transfornation_config

        except Exception as e:
            raise SensorException(e, sys)
        
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)
        

    @classmethod
    def get_data_transformer_object(cls) ->Pipeline:
        try:
            logging.info("transforming the Data using Robust_scaler and Simple_imputer")
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="mean")
            preprocessor = Pipeline(
                steps = [
                    ('imputer',simple_imputer),
                    ('robust_scaler', robust_scaler)
                ]
            )
            return preprocessor

        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Data transformation started")

            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            preprocessor = self.get_data_transformer_object()
            
            #training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            
            target_feature_train_df = train_df[TARGET_COLUMN]

            target_feature_train_df = target_feature_train_df.replace( TargetValueMapping().to_dict()).infer_objects(copy=False)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = test_df[TARGET_COLUMN]

            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict()).infer_objects(copy=False)

            #applying fit and transform 
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            # applying smote for imbalance data
            smt = SMOTETomek(sampling_strategy="minority", n_jobs=-1)

            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df)

            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_test_feature, target_feature_test_df)

            #data combination
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            #preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            logging.info(f"data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact

            
        except Exception as e:
            raise SensorException(e, sys)

