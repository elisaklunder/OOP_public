import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sounddevice as sd

sys.path.append(os.getcwd() + "/src/")
from src.audio_classification_dataset import AudioClassificationDataset
from src.audio_pitchshift import PitchShifting
from src.audio_regression_dataset import (
    AudioRegressionDataset,  # never used --> REPORT!!
)
from src.audio_resampling import Resampling
from src.batchloader import BatchLoader
from src.image_center_crop import ImageCenterCrop
from src.image_classification_dataset import (
    ImageClassificationDataset,  # never used --> REPORT!!
)
from src.image_patching import ImagePatching
from src.image_regression_dataset import ImageRegressionDataset
from src.preprocessing_pipeline import PreprocessingPipeline


def main():

    # # DATASETS # #

    # # IMAGE REGRESSION DATASET
    # img_regr_dataset = ImageRegressionDataset()
    # img_regr_root = r"C:\Users\elikl\Documents\Università\yr2\2 - OOP\oop-final-project-group-7\image_regression_csv\images_poly"
    # img_regr_labels_path = r"C:\Users\elikl\Documents\Università\yr2\2 - OOP\oop-final-project-group-7\image_regression_csv\poly_targets_regression.csv"

    # # EAGER LOADING WITHOUT LABELS
    # img_regr_dataset.load_data(
    #     root=img_regr_root, strategy="eager", format="csv"
    # )
    # image = img_regr_dataset[1]
    # image = Image.fromarray(image)
    # image.show()

    # # LAZY LOADING WITH LABELS
    # img_regr_dataset.load_data(
    #     root=img_regr_root,
    #     strategy="lazy",
    #     format="csv",
    #     labels_path=img_regr_labels_path,
    # )
    # image, target = img_regr_dataset[1]
    # # different image than before because the images are now ordered based on
    # # the csv file
    # image = Image.fromarray(image)
    # image.show()
    # print(f"Degrees of rotation of the polygon: {target}")

    # # SPLITTING IN TRAIN AND TEST WITHOUT SHUFFLING
    # img_train, img_test = img_regr_dataset.train_test_split(
    #     train_size=0.6, shuffle=False
    # )
    # print(f"Size of the image regression dataset: {len(img_regr_dataset)}")
    # # 10000
    # print(f"Size of the image train dataset: {len(img_train)}")
    # # 6000
    # print(f"Size of the image test dataset: {len(img_test)}")
    # # 4000

    # AUDIO DATASETS
    # in the following section we will showcase the loading of two types of datasets: one in a hierarchical structure and one in a .csv format. We show the eager loading only once as it is computationally more expensive to perform. Also the the Batchloading and the Pipeline are shown only once since they work in the same way regardless of the initial structure of the data.

    # AUDIO CLASSIFICATION DATASET
    aud_clas_dataset = AudioClassificationDataset()
    aud_clas_root = "/Users/juliabelloni/Desktop/oop/assignments/oop-final-project-group-7/audio_classification_hierarchy"

    aud_regr_dataset = AudioRegressionDataset()
    aud_regr_root = "/Users/juliabelloni/Desktop/oop/assignments/oop-final-project-group-7/audio_regression_csv/TRAIN"
    aud_regr_labels_path = "/Users/juliabelloni/Desktop/oop/assignments/oop-final-project-group-7/audio_regression_csv/TRAIN.csv"



    # LAZY LOADING
    # loading data from .csv format lazily
    aud_regr_dataset.load_data(
        root=aud_regr_root, strategy="lazy", format="csv", labels_path=aud_regr_labels_path
    )
    # play original audio
    print(aud_regr_dataset[3])
    audio, target = aud_regr_dataset[3]
    sample, sr = audio
    sd.play(sample, sr)
    sd.wait()
    print(f"The target is:' {target}'")

    # loading dataset in hierarchical format lazily
    aud_clas_dataset.load_data(
        root=aud_clas_root, strategy="lazy", format="hierarchical"
    )

    # play original audio
    print(aud_clas_dataset[3])
    audio, target = aud_clas_dataset[3]
    sample, sr = audio
    sd.play(sample, sr)
    sd.wait()
    print(f"The target is:' {target}'")

    # EAGER LOADING
    # reloading dataset in hierarchical format eagerly
    aud_clas_dataset.load_data(
        root=aud_clas_root, strategy="eager", format="hierarchical"
    )

    # play original audio
    print(aud_clas_dataset[3])
    audio, target = aud_clas_dataset[3]
    sample, sr = audio
    sd.play(sample, sr)
    sd.wait()
    print(f"The target is:' {target}'")

    # SPLITTING IN TRAIN AND TEST WITH SHUFFLING
    aud_train, aud_test = aud_clas_dataset.train_test_split(
        train_size=0.6, shuffle=True
    )
    print(f"Size of the audio classification dataset: {len(aud_clas_dataset)}")
    print(f"Size of the train dataset: {len(aud_train)}")
    print(f"Size of the test dataset: {len(aud_test)}")

    # BATCHLOADERS #

    # # IMAGE BATCHLOADER IN SEQUENTIAL FASHION WITHOUT DISCARDING
    # img_batcher = BatchLoader()
    # img_batcher.create_batches(
    #     dataset=img_train,
    #     batch_size=130,
    #     batch_style="sequential",
    #     discard_last_batch=False,
    # )

    # print(f"Number of batches created: {len(img_batcher)}")
    # 6000/130=46.2=47 becasue discard_last_batch=False

    # img_batch = next(img_batcher)
    # print(f"Length of the first batch is: {len(img_batch)}")
    # 130

    # last_batch = None
    # for img_batch in img_batcher:
    #     last_batch = img_batch
    # print(f"Length of the last batch is: {len(last_batch)}")
    # 20 because 6000-(130*46)=20

    # AUDIO BATCHLOADER IN RANDOM FASHION WITH DISCARDING
    aud_batcher = BatchLoader()
    aud_batcher.create_batches(
        dataset=aud_train,
        batch_size=100,  # set something that makes sense,
        batch_style="random",
        discard_last_batch=True,
    )

    print(f"Number of batches created: {len(aud_batcher)}")
    # calculate whats gonna be printed

    aud_batch = next(aud_batcher)
    print(f"Length of the first batch is: {len(aud_batch)}")
    # length of batch u chose

    last_batch = None
    for aud_batch in aud_batcher:
        last_batch = aud_batch
    print(f"Length of the last batch is: {len(last_batch)}")
    # last batch has the same length of every other batch

    # # PIPELINES #

    # # IMAGE PREPROCESSING PIPELINE
    # image, target = img_regr_dataset[5]
    # image_show = Image.fromarray(image)
    # image_show.show()  # show original image

    # # define pipeline
    # crop = ImageCenterCrop(70, 100)
    # patch = ImagePatching("red", 30, 30)
    # img_pipeline = PreprocessingPipeline(crop, patch)

    # # apply pipeline
    # preprocessed_image = img_pipeline(image)
    # preprocessed_image_show = Image.fromarray(preprocessed_image)
    # preprocessed_image_show.show()  # show preprocessed image

    # AUDIO PREPROCESSING PIPELINE
    audio, target = aud_clas_dataset[10]

    # define pipeline
    pitch_shift = PitchShifting(100)
    resample = Resampling(6000)
    aud_pipeline = PreprocessingPipeline(pitch_shift, resample)

    # apply pipeline
    processed_audio_samples, processed_audio_s_rate = aud_pipeline(audio)

    # play audio after pitch shifting and resampling
    print("Audio signal after preprocessing steps were applied")
    sd.play(processed_audio_samples, processed_audio_s_rate)
    sd.wait()


if __name__ == "__main__":
    main()
