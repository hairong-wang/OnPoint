## [Project Demo Slides](https://docs.google.com/presentation/d/16pl_ZvUmtmWsFKmMWbTw3GtJ1R5X2A84t0INaWZ02Ek/edit#slide=id.g63c4d69c00_0_222)
## [Package](https://pypi.org/project/onpoint/)

# OnPoint: A Question Answering Service leveraging user reviews
![image of pipline](https://github.com/hairong-wang/XLNet_learn2learn/blob/dev-tpu_version-20191012/src/com/insightdatascience/xlnet_learn2learn/static/img/pipeline.png)

OnPoint is a question answering service which levearages product user reviews. OnPoint saves you lots of time when you try to look for a product detail by providing you a short answer in seconds.

<p align="center">
<img src="https://github.com/hairong-wang/XLNet_learn2learn/blob/dev-tpu_version-20191012/src/com/insightdatascience/xlnet_learn2learn/static/img/demo-gif.gif">
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
Everything needed fot the environment

## Steps to run

### Step1: Configuration

### Step2: Prepare and Preprocess
#### - Download dataset
Download the dataset you want to use for finetuning.
The datasets used in this project are:
- **The [Squad dataset](https://rajpurkar.github.io/SQuAD-explorer/) is used in this proeject.**
- **The manual sampled and labeled AmazonQA and preprocessed dataset is available [here]**

#### - Download model checkpoints
- The model checkpoints is available [here]()

#### - Convert dataset to SQuAD format(Optional)
If you want to try other dataset, it needs to be converted to SQuAD format first.
```
code for converting to squad
```
#### - Preprocess data
```
```
### Step3: Train model
```
bash scripts/tpu_run_squad.sh
```

### Step4: Evaluate model

### Step5: Inference model

### Step6: run the flask app on your local machine
```

```

## Analysis

#### Final result:

Model | Finetune Dataset | Validation Dataset | AmazonQA Sample Coverage | F1
------|------------------|--------------------|--------------------------|---
BERT-Large | SQuAD 2.0 | Augmented AmazonQA | 30% | 67.34
XLNet-Large | SQuAD 2.0 | Augmented AmazonQA | 40% | 66.20
XLNet-Large | Augmented AmazonQA | Augmented AmazonQA | 0% | 66.67
XLNet-Large | SQuAD 2.0 + Augmented AmazonQA | Augmented AmazonQA | 50% | 69.27
