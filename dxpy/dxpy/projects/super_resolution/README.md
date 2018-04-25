# Instructions about Enhancing the image quality via transferred deep residual learning of coarse PET sinograms
## Prerequirements
[Tensorflow](https://www.tensorflow.org/)
[Astra-toolbox](http://www.astra-toolbox.com/)

## Install

Run in shell:
`pip install dxl-dxpy`

## Code

### Dataset
`dxl.lean.dataset.super_resolution`

### Network
`dxl.learn.net.zoo.srms`

## Command line tools:

### Training

`dxpy ln train_dist -j master/worker -t 0..N`
Please use `dxpy ln train_dist --help` for details.

### Inference
`dxpy ln infer -t TASK_NAME -d DATASET_DIR -o OUTPUT_FILE -n NUMBER_OF_SAMPLES` 

### Reconstruction
`dxpy ln infer -t TASK_NAME -d DATASET_DIR -o OUTPUT_FILE -n NUMBER_OF_SAMPLES`

