# coding: utf8
# author: Hairong Wang

from flask import Flask, request, render_template
import logging
import os
import collections
import six
import json
import time
import datetime
import tensorflow as tf
import sentencepiece as spm
from onpoint import model_utils
from onpoint.run_squad import read_squad_examples, _get_spm_basename, FeatureWriter, convert_examples_to_features, \
    input_fn_builder, get_model_fn, FLAGS, write_predictions

if six.PY2:
    import cPickle as pickle
else:
    import pickle

app = Flask(__name__)


def setup_app(app):
    '''set up some global configuration before defining other functions in the app'''
    global FLAGS, sp_model, model_fn, run_config, estimator, spm_basename, eval_writer, eval_rec_file, \
        eval_feature_file
    FLAGS.num_core_per_host = 1
    FLAGS.model_config_path = os.path.join('model/xlnet_cased_L-24_H-1024_A-16', 'xlnet_config.json')
    FLAGS.spiece_model_file = os.path.join('model/xlnet_cased_L-24_H-1024_A-16', 'spiece.model')
    FLAGS.output_dir = 'proc_data'
    FLAGS.init_checkpoint = os.path.join('model/finetuned', 'model.ckpt-4000')
    FLAGS.model_dir = 'model/finetuned'
    FLAGS.predict_file = 'tmp/data.json'
    FLAGS.predict_dir = 'tmp'
    FLAGS.do_train = False
    FLAGS.do_predict = True
    FLAGS.overwrite_data = True
    FLAGS.predict_batch_size = 16

    sp_model = spm.SentencePieceProcessor()
    sp_model.Load(FLAGS.spiece_model_file)

    model_fn = get_model_fn()
    run_config = model_utils.configure_tpu(FLAGS)

    estimator = tf.estimator.Estimator(
        model_fn=model_fn,
        config=run_config)

    spm_basename = _get_spm_basename()

    eval_rec_file = os.path.join(
        FLAGS.output_dir,
        "{}.slen-{}.qlen-{}.eval.tf_record".format(
            spm_basename, FLAGS.max_seq_length, FLAGS.max_query_length))
    eval_feature_file = os.path.join(
        FLAGS.output_dir,
        "{}.slen-{}.qlen-{}.eval.features.pkl".format(
            spm_basename, FLAGS.max_seq_length, FLAGS.max_query_length))

    eval_writer = FeatureWriter(filename=eval_rec_file, is_training=False)

    logging.basicConfig(filename='app.log', level=logging.INFO)


@app.route("/")
def html_display():
    '''render html for root url'''
    return render_template("index.html")


@app.route("/query", methods=['POST'])
def get_result():
    '''
    Get answer for the question based on the context

    Returns:
        result (json str) -- a json string containing answer dictionary
    '''
    start_time = time.time()
    query = str(request.form['query_text'])
    query_text = query
    context_text = str(request.form['context_text'])
    result = process_query_wrapper(query_text, context_text)
    end_time = time.time()
    answer = json.loads(result)["answer"]
    log_file = open('query_records.log', 'a')
    log_file.write("Start Time: " + str(
        datetime.datetime.now()) + "; Query: " + query_text + "; Answer: " + answer + "; Time Used: " + str(
        end_time - start_time) + '\n')
    log_file.close()
    duration = str(end_time - start_time)
    print('time used = ', duration)
    return result


def process_query(query_text: str, context_text: str):
    if query_text is None:
        return None
    answer = 'No answer found'
    try:
        # convert context to squad test dataset format
        context = {"version": "v2.0",
                   "data": [{"title": "user_context",
                             "paragraphs": [{"qas": [{"question": query_text,
                                                      "id": "test",
                                                      "answers": []}],
                                             "context": context_text}]}]}

        # FLAGS.num_core_per_host = 1
        # FLAGS.model_config_path = os.path.join('model/xlnet_cased_L-24_H-1024_A-16','xlnet_config.json')
        # FLAGS.spiece_model_file = os.path.join('model/xlnet_cased_L-24_H-1024_A-16', 'spiece.model')
        # FLAGS.output_dir = 'proc_data'
        # FLAGS.init_checkpoint = os.path.join('model/finetuned','model.ckpt-4000')
        # FLAGS.model_dir = 'model/finetuned'
        # FLAGS.predict_file = 'tmp/data.json'
        # FLAGS.predict_dir = 'tmp'
        # FLAGS.do_train = False
        # FLAGS.do_predict = True
        # FLAGS.overwrite_data = True
        # FLAGS.predict_batch_size = 16

        with open(FLAGS.predict_file, 'w') as f:
            json.dump(context, f)
            f.close()

        # sp_model = spm.SentencePieceProcessor()
        # sp_model.Load(FLAGS.spiece_model_file)

        RawResult = collections.namedtuple("RawResult",
                                           ["unique_id", "start_top_log_probs", "start_top_index",
                                            "end_top_log_probs", "end_top_index", "cls_logits"])

        # model_fn = get_model_fn()
        # run_config = model_utils.configure_tpu(FLAGS)

        # estimator = tf.estimator.Estimator(
        #     model_fn=model_fn,
        #     config=run_config)

        # spm_basename = _get_spm_basename()

        eval_examples = read_squad_examples(FLAGS.predict_file, is_training=False)

        with tf.gfile.Open(FLAGS.predict_file) as f:
            orig_data = json.load(f)["data"]

        # eval_rec_file = os.path.join(
        #     FLAGS.output_dir,
        #     "{}.slen-{}.qlen-{}.eval.tf_record".format(
        #         spm_basename, FLAGS.max_seq_length, FLAGS.max_query_length))
        # eval_feature_file = os.path.join(
        #     FLAGS.output_dir,
        #     "{}.slen-{}.qlen-{}.eval.features.pkl".format(
        #         spm_basename, FLAGS.max_seq_length, FLAGS.max_query_length))

        # eval_writer = FeatureWriter(filename=eval_rec_file, is_training=False)
        eval_features = []

        def append_feature(feature):
            eval_features.append(feature)
            eval_writer.process_feature(feature)

        convert_examples_to_features(
            examples=eval_examples,
            sp_model=sp_model,
            max_seq_length=FLAGS.max_seq_length,
            doc_stride=FLAGS.doc_stride,
            max_query_length=FLAGS.max_query_length,
            is_training=False,
            output_fn=append_feature)
        eval_writer.close()

        with tf.gfile.Open(eval_feature_file, 'wb') as fout:
            pickle.dump(eval_features, fout)

        eval_input_fn = input_fn_builder(
            input_glob=eval_rec_file,
            seq_length=FLAGS.max_seq_length,
            is_training=False,
            drop_remainder=False,
            num_hosts=1)

        cur_results = []

        for result in estimator.predict(
                input_fn=eval_input_fn,
                yield_single_examples=True):

            if len(cur_results) % 1000 == 0:
                tf.logging.info("Processing example: %d" % (len(cur_results)))

            unique_id = int(result["unique_ids"])
            start_top_log_probs = (
                [float(x) for x in result["start_top_log_probs"].flat])
            start_top_index = [int(x) for x in result["start_top_index"].flat]
            end_top_log_probs = (
                [float(x) for x in result["end_top_log_probs"].flat])
            end_top_index = [int(x) for x in result["end_top_index"].flat]

            cls_logits = float(result["cls_logits"].flat[0])

            cur_results.append(
                RawResult(
                    unique_id=unique_id,
                    start_top_log_probs=start_top_log_probs,
                    start_top_index=start_top_index,
                    end_top_log_probs=end_top_log_probs,
                    end_top_index=end_top_index,
                    cls_logits=cls_logits))

        output_prediction_file = os.path.join(
            FLAGS.predict_dir, "predictions.json")
        output_nbest_file = os.path.join(
            FLAGS.predict_dir, "nbest_predictions.json")
        output_null_log_odds_file = os.path.join(
            FLAGS.predict_dir, "null_odds.json")

        ret = write_predictions(eval_examples, eval_features, cur_results,
                                FLAGS.n_best_size, FLAGS.max_answer_length,
                                output_prediction_file,
                                output_nbest_file,
                                output_null_log_odds_file,
                                orig_data)
        prediction = {}
        with open(output_prediction_file) as f:
            prediction = json.load(f)
            f.close()
        answer = prediction['test']

    except Exception as e:
        logging.error(e)
    return answer


def process_query_wrapper(query_text: str, context_text: str):
    '''
    Wrapper for function 'process_query'

    Args:
        query_text (str) -- a question provided by user
        context_text (str) -- a paragraph from some article provided by user

    Returns:
        response (json str) -- a json string containing answer dictionary
    '''
    answer = process_query(query_text, context_text)
    response = json.dumps({"answer": answer})
    return response


def main(_):
    setup_app(app)
    app.run(port=6001, debug=True)


if __name__ == '__main__':
    # parse FLAGS and run the main function
    tf.app.run()
