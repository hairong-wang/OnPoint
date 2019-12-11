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
1. tensorflow==1.15
2. absl-py==0.8.0
3. Flask==1.1.1
4. pip
5. sentencepiece

#### Operating system
Linux

#### Environment setup
Optional, if you have multiple GPUs on your machine, then it's recommended that you use one GPU to run. Without this configuration, it might take unnecessary memory from addtional GPUs while this additional GPUs are not actually running. 
```
export CUDA_VISIBLE_DEVICES=0
```

## Steps to run the Flask App
### Step1: Install requirement
run
```
pip install -r requirement.txt
```

### Step2: Download dataset and model checkpoints

#### - Download dataset
The datasets used in this project are:
- **The [Squad dataset](https://rajpurkar.github.io/SQuAD-explorer/) is used in this proeject.**
- **The manual sampled and labeled AmazonQA and preprocessed dataset is available at Google Cloud Storage Buckets/xlnet_squad2/data/amazon, you can access the bucket from [here](https://console.cloud.google.com/storage/browser/xlnet_squad2).**
Download the datasets for finetuning by running the following:
```
cd onpoint
bin/data_ingestion
```

#### - Download model checkpoints
- The model checkpoints is available at Google Cloud Storage Buckets/xlnet_squad2/experiment/squad_and_amazon_8000steps_1000warmup, you can access the bucket from [here](https://console.cloud.google.com/storage/browser/xlnet_squad2).
So far, the top performance model checkpoint is 'model.ckpt-4000'
Download the model checkpoints by running:
```
bin/model_download
```

### Step3: Run the app
```
python3 app.py
```
Open your browser, and enter:
```
localhost:6001
```
Now you can paste the context you want to use to the left text box, and type in the question to the right text box.


## Steps to finetune the model
Please log in to GCP compute engine instance for the following steps.
For finetuning, you'll need a TPU instance and GCP storage bucket.

### Step0: Download datasets and models(see above)

###Step1: Data processing
#### - Convert dataset to SQuAD format(Optional)
If you want to try other dataset, it needs to be converted to SQuAD format first using squad_converter.py
```
# Change the INFILE and OUTFILE path
python3 squad_converter.py
```
#### - Preprocess data
multi-processing available in bin/data_processing, need to change 'NUM_PROC=' to the number of core you'll use.
Replace with your own gcp storage bucket
```
cd onpoint
export STORAGE_BUCKET=${YOUR GCP STORAGE BUCKET}
bin/data_processing
```
### Step2: Train model
The model_building script contains two parts, the second part is for fintuning on Amazon, now it's commented.
If you want to finetune on AmazonQA, please comment the first part, and uncomment the second part.
please replace with your own tpu name
```
export TPU_NAME=${YOUR TPU NAME}
bin/model_building
```
### Step3: Evaluate model
The model_analysis script is to evaluate the model fintuned on SQUAD. If you'd like to evaluate other checkpoints, please modify the variables
```
export STORAGE_BUCKET=${YOUR GCP STORAGE BUCKET}
export TPU_NAME=${YOUR TPU NAME}
bin/model_analysis
```
### Step4: Inference model
Model inference takes two arguments, the first is the path name of the test dataset in JSON format, the second is the folder name of output(prediction) directory
You can find the following folders in the tmp folder:
null_odds.json: no answer probability
nbest_predictions.json: the top n result, n can be set in run_squad.py
```
flags.DEFINE_integer("n_best_size", default=5,
                     help="n best size for predictions")
```
predictions.json: top 1 prediction results

```
bin/model_inference ${TEST DATASET JSON PATH NAME} ${OUTPUT FOLDER NAME}
```

## Analysis

#### Final result:

| Model       |Finetune Dataset| Validation Dataset |AmazonQA Sample Coverage| F1|
| :---        |:---:            |:---:               |:---:                  |:---:|
| BERT-Large  |SQuAD 2.0.       |Augmented AmazonQA | 30%                    | 67.34|
| XLNet-Large |SQuAD 2.0.       | Augmented AmazonQA | 40%                   | 66.20|
| XLNet-Large |Augmented AmazonQA|Augmented AmazonQA | 0%                    | 66.67|
| XLNet-Large |SQuAD 2.0 + Augmented AmazonQA|Augmented AmazonQA| 50%        | 69.27|



