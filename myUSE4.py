import tensorflow as tf
import tensorflow_hub as hub



embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

embeddings = tf.make_ndarray(tf.make_tensor_proto(embed(["Twinkle Twinkle little stars."]))).tolist()[0]


print(type(embeddings))

print(len(embeddings))

print(embeddings)


