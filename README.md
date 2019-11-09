## [Project Demo Slides](https://docs.google.com/presentation/d/16pl_ZvUmtmWsFKmMWbTw3GtJ1R5X2A84t0INaWZ02Ek/edit#slide=id.g63c4d69c00_0_222)
## [Package](https://pypi.org/project/onpoint/): new release coming soon.

# OnPoint: A Question Answering Service leveraging user reviews
![image of pipline](https://github.com/hairong-wang/OnPoint/blob/master/onpoint/static/img/pipeline.png)

OnPoint is a question answering service which levearages product user reviews. OnPoint saves you lots of time when you try to look for a product detail by providing you a short answer in seconds.

<p align="center">
<img src="https://github.com/hairong-wang/OnPoint/blob/master/onpoint/static/img/demo-gif.gif">
</p>

This repository explores the application of XL-Net on user review based question answering service. The base model and algorithm was inspired and based upon the [XLNet: Generalized Autoregressive Pretraining for Language Understanding link](https://github.com/zihangdai/xlnet) and [renatoviolin/xlnet link](https://github.com/renatoviolin/xlnet) repo.

## The directory structure of this repo is the following:
- **onpoint** : contains all the source code
- **tst** : contains all the unit tests
  - **data** : contains data for unit test
- **configs** : contains config files for hyperparameters during finetuning and evaluation

## Setup

#### Installation
```
git clone https://github.com/hairong-wang/OnPoint.git
cd OnPoint
```
#### Requisites
1. tensorflow-gpu==1.15.0-rc1
2. absl-py==0.8.0
3. Flask==1.1.1
4. pip

#### Environment setup
```
export CUDA_VISIBLE_DEVICES=0
```

## Steps to run

### Step1: Configuration
All files in OnPoint/onpoint/bin need configuration.
Here's one example to change path:
```
SQUAD_DATA_S3_BUCKET='squad-data'
SQUAD_DATA_TRAIN_S3_KEY='squad2.0/train-v2.0.json'
SQUAD_DATA_DEV_S3_KEY='squad 2.0/dev-v2.0.json'
LOCAL_SQUAD_DATA_TRAIN_PATH=./squad2.0_train.json
LOCAL_SQUAD_DATA_DEV_PATH=./squad2.0_dev.json
MODEL_DIR=YOUR PATH
```

### Step2: Prepare and Preprocess
#### - Download dataset
Download the dataset you want to use for finetuning.
The datasets used in this project are:
- **The [Squad dataset](https://rajpurkar.github.io/SQuAD-explorer/) is used in this proeject.**
- **The manual sampled and labeled AmazonQA and preprocessed dataset is available at Google Cloud Storage Buckets/xlnet_squad2/data/amazon, you can access the bucket from [here](https://console.cloud.google.com/storage/browser/xlnet_squad2).**

#### - Download model checkpoints
- The model checkpoints is available at Google Cloud Storage Buckets/xlnet_squad2/experiment/squad_and_amazon_8000steps_1000warmup, you can access the bucket from [here](https://console.cloud.google.com/storage/browser/xlnet_squad2).
So far, the top performance model checkpoint is 'model.ckpt-4000'
The following files need to be downloaded and put in your path accordingly.
<p align="center">
<img src="https://github.com/hairong-wang/OnPoint/blob/master/onpoint/static/img/download_files.png">
</p>

#### - Convert dataset to SQuAD format(Optional)
If you want to try other dataset, it needs to be converted to SQuAD format first.
```
# Change the INFILE and OUTFILE path
python3 squad_converter.py
```
#### - Preprocess data
multi-processing available, need to change 'NUM_PROC=' to the number of core you'll use.
```
cd onpoint
bash bin/data_processing
```
### Step3: Train model
```
bash bin/model_building
```
### Step4: Evaluate model
```
bash bin/model_analysis
```
### Step5: Inference model
```
bash bin/model_inference
```
### Step6: run the flask app on your local machine
```
python3 app.py
```

## Analysis

#### Final result:

| Model       |Finetune Dataset| Validation Dataset |AmazonQA Sample Coverage| F1|
| :---        |:---:            |:---:               |:---:                  |:---:|
| BERT-Large  |SQuAD 2.0.       |Augmented AmazonQA | 30%                    | 67.34|
| XLNet-Large |SQuAD 2.0.       | Augmented AmazonQA | 40%                   | 66.20|
| XLNet-Large |Augmented AmazonQA|Augmented AmazonQA | 0%                    | 66.67|
| XLNet-Large |SQuAD 2.0 + Augmented AmazonQA|Augmented AmazonQA| 50%        | 69.27|



