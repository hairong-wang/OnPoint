import boto3
from absl import flags

# Preprocessing
flags.DEFINE_bool("s3_bucket", default=False,
      help="S3 bucket for dataset.")
flags.DEFINE_integer("s3_key", default=16,
      help="S3 object key for the dataset.")
flags.DEFINE_integer("local_path", default=0,
      help="Local path to store downloaded dataset.")

def download_data_from_s3():
    download_helper(flags.s3_bucket,
                    flags.s3_key,
                    flags.local_path)

def download_helper(bucket,
                    key,
                    output_path):
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=bucket,
                               Key=key)
    data = obj['Body'].read().decode('utf-8')
    file_head = open(output_path, 'w')
    file_head.write(data)
    file_head.close()

if __name__ == '__main__':
    download_data_from_s3()
