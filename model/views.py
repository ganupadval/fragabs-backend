from spacy.lang.en import English
import os
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder as label_encoder
import tensorflow_hub as hub
import tensorflow_text as text
import numpy as np
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# model_cache_key = 'model_cache'
file_name = 'utils/model.h5'
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, file_name)
# model = cache.get(model_cache_key)

# if model is None:
#     model = tf.keras.models.load_model(
#     (file_path),
#     custom_objects={'KerasLayer': hub.KerasLayer})
# # save in django memory cache
# cache.set(model_cache_key, model, None)

model = tf.keras.models.load_model(
(file_path),
custom_objects={'KerasLayer': hub.KerasLayer})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fragment(request):

    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        sentence = request_data.get('sentence')
        # setup English sentence parser
        nlp = English()
        # create sentence splitting pipeline object
        sentencizer = nlp.create_pipe("sentencizer")
        # add sentence splitting pipeline object to sentence parser
        nlp.add_pipe('sentencizer')
        # create "doc" of parsed sequences, change index for a different abstract
        doc = nlp(sentence)
        # return detected sentences from doc in string type (not spaCy token type)
        abstract_lines = [str(sent) for sent in list(doc.sents)]
        total_lines_in_sample = len(abstract_lines)

        # Go through each line of abstract and create a list of dictionary containing features for each line
        sample_lines = []
        for i, line in enumerate(abstract_lines):
            sample_dict = {}
            sample_dict["text"] = str(line)
            sample_dict["line_number"] = i
            sample_dict["total_lines"] = total_lines_in_sample - 1
            sample_lines.append(sample_dict)

        # Get all line nmuber values from sample abstract
        test_abstract_line_number = [line["line_number"]
                                     for line in sample_lines]
        # One hot encode them to same depth as training data
        test_abstract_line_number_onehot = tf.one_hot(
            test_abstract_line_number, depth=15)

        # Get all total lines value from sample dict
        test_abstract_total_lines = [line["total_lines"]
                                     for line in sample_lines]
        # One hot encode them to same depth as training data
        test_abstract_total_lines_onehot = tf.one_hot(
            test_abstract_total_lines, depth=20)

        test_abstract_pred_probs = model.predict(x=(test_abstract_line_number_onehot,
                                                  test_abstract_total_lines_onehot,
                                                  tf.constant(abstract_lines)))

        test_abstract_preds = tf.argmax(test_abstract_pred_probs, axis=1)

        class_names = np.array(['BACKGROUND', 'CONCLUSIONS',
                                'METHODS', 'OBJECTIVE', 'RESULTS'], dtype="object")

        test_abstract_pred_classes = [
            class_names[i] for i in test_abstract_preds]

        new_list = []
        new_dict = {}
        for i, line in enumerate(abstract_lines):
            if (test_abstract_pred_classes[i] == "OBJECTIVE"):
                if "OBJECTIVE" in new_dict.keys():
                    new_dict["OBJECTIVE"] += [line]
                else:
                    new_dict["OBJECTIVE"] = []
                    new_dict["OBJECTIVE"] += [line]
            if (test_abstract_pred_classes[i] == "BACKGROUND"):
                if "BACKGROUND" in new_dict.keys():
                    new_dict["BACKGROUND"] += [line]
                else:
                    new_dict["BACKGROUND"] = []
                    new_dict["BACKGROUND"] += [line]
            if (test_abstract_pred_classes[i] == "METHODS"):
                if "METHODS" in new_dict.keys():
                    new_dict["METHODS"] += [line]
                else:
                    new_dict["METHODS"] = []
                    new_dict["METHODS"] += [line]
            if (test_abstract_pred_classes[i] == "RESULTS"):
                if "RESULTS" in new_dict.keys():
                    new_dict["RESULTS"] += [line]
                else:
                    new_dict["RESULTS"] = []
                    new_dict["RESULTS"] += [line]
            if (test_abstract_pred_classes[i] == "CONCLUSIONS"):
                if "CONCLUSIONS" in new_dict.keys():
                    new_dict["CONCLUSIONS"] += [line]
                else:
                    new_dict["CONCLUSIONS"] = []
                    new_dict["CONCLUSIONS"] += [line]

        # close = print(f"{test_abstract_pred_classes[i]}: {line}")
        new_list.append(new_dict)
        ans = new_list
        # print(ans)

        return JsonResponse(ans, safe=False)
