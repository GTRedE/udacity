
# coding: utf-8

# # Self-Driving Car Engineer Nanodegree
# 
# ## Deep Learning
# 
# ## Project: Build a Traffic Sign Recognition Classifier
# 
# In this notebook, a template is provided for you to implement your functionality in stages, which is required to successfully complete this project. If additional code is required that cannot be included in the notebook, be sure that the Python code is successfully imported and included in your submission if necessary. 
# 
# > **Note**: Once you have completed all of the code implementations, you need to finalize your work by exporting the iPython Notebook as an HTML document. Before exporting the notebook to html, all of the code cells need to have been run so that reviewers can see the final implementation and output. You can then export the notebook by using the menu above and navigating to  \n",
#     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission. 
# 
# In addition to implementing code, there is a writeup to complete. The writeup should be completed in a separate file, which can be either a markdown file or a pdf document. There is a [write up template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) that can be used to guide the writing process. Completing the code template and writeup template will cover all of the [rubric points](https://review.udacity.com/#!/rubrics/481/view) for this project.
# 
# The [rubric](https://review.udacity.com/#!/rubrics/481/view) contains "Stand Out Suggestions" for enhancing the project beyond the minimum requirements. The stand out suggestions are optional. If you decide to pursue the "stand out suggestions", you can include the code in this Ipython notebook and also discuss the results in the writeup file.
# 
# 
# >**Note:** Code and Markdown cells can be executed using the **Shift + Enter** keyboard shortcut. In addition, Markdown cells can be edited by typically double-clicking the cell to enter edit mode.

# ---
# ## Step 0: Load The Data

# In[1]:


# Load pickled data
import pickle

training_file = 'data/train.p'
validation_file= 'data/valid.p'
testing_file = 'data/test.p'

with open(training_file, mode='rb') as f:
    train = pickle.load(f)
with open(validation_file, mode='rb') as f:
    valid = pickle.load(f)
with open(testing_file, mode='rb') as f:
    test = pickle.load(f)
    
X_train, y_train = train['features'], train['labels']
X_valid, y_valid = valid['features'], valid['labels']
X_test, y_test = test['features'], test['labels']


# ---
# 
# ## Step 1: Dataset Summary & Exploration
# 
# The pickled data is a dictionary with 4 key/value pairs:
# 
# - `'features'` is a 4D array containing raw pixel data of the traffic sign images, (num examples, width, height, channels).
# - `'labels'` is a 1D array containing the label/class id of the traffic sign. The file `signnames.csv` contains id -> name mappings for each id.
# - `'sizes'` is a list containing tuples, (width, height) representing the original width and height the image.
# - `'coords'` is a list containing tuples, (x1, y1, x2, y2) representing coordinates of a bounding box around the sign in the image. **THESE COORDINATES ASSUME THE ORIGINAL IMAGE. THE PICKLED DATA CONTAINS RESIZED VERSIONS (32 by 32) OF THESE IMAGES**
# 
# Complete the basic data summary below. Use python, numpy and/or pandas methods to calculate the data summary rather than hard coding the results. For example, the [pandas shape method](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.shape.html) might be useful for calculating some of the summary results. 

# ### Provide a Basic Summary of the Data Set Using Python, Numpy and/or Pandas

# In[2]:


### Use python, pandas or numpy methods rather than hard coding the results
import numpy as np

# TODO: Number of training examples
n_train = len(X_train)

# TODO: Number of validation examples
n_valid = len(X_valid)

# TODO: Number of testing examples.
n_test = len(X_test)

# TODO: What's the shape of a traffic sign image?
image_shape = X_train.shape[1:]

# TODO: How many unique classes/labels there are in the dataset.
labels_index = np.unique(y_train)
n_labels = len(labels_index)

print("Number of training examples =", n_train)
print("Number of validation examples =", n_valid)
print("Number of testing examples =", n_test)
print("Image data shape =", image_shape)
print("Number of labels/classes =", n_labels)


# ### Include an exploratory visualization of the dataset

# Visualize the German Traffic Signs Dataset using the pickled file(s). This is open ended, suggestions include: plotting traffic sign images, plotting the count of each sign, etc. 
# 
# The [Matplotlib](http://matplotlib.org/) [examples](http://matplotlib.org/examples/index.html) and [gallery](http://matplotlib.org/gallery.html) pages are a great resource for doing visualizations in Python.
# 
# **NOTE:** It's recommended you start with something simple first. If you wish to do more, come back to it after you've completed the rest of the sections. It can be interesting to look at the distribution of classes in the training, validation and test set. Is the distribution the same? Are there more examples of some classes than others?

# In[ ]:


## Show random image and label index

import random
import matplotlib.pyplot as plt 

# Show visualizations in the notebook
get_ipython().magic('matplotlib inline')

index = random.randint(0, len(X_train))
image = X_train[index].squeeze()

plt.figure(figsize=(1,1))
plt.imshow(image, cmap="gray")
print('label index: ', y_train[index])


# #### Complete set of images and labels

# In[ ]:


# Create label dictionary {label:signname}
import csv
    
labels_dict = None
with open('signnames.csv', mode='r') as infile:
    reader = csv.reader(infile)
    next(reader, None)
    labels_dict = {int(rows[0]):rows[1] for rows in reader}


# In[ ]:


print(labels_dict)


# In[ ]:


fig = plt.figure(figsize=(22,35), tight_layout={'h_pad':5})

for i in range(n_labels):
    image_key = np.where(y_train==i)
    img = X_train[image_key[0][0]]
    ax = fig.add_subplot(int(n_labels/4)+1,4,i+1) 
    ax.imshow(img, interpolation='none')
    plt.title("[%02d] %s" % (i, labels_dict[y_train[image_key[0][0]]]))
plt.show()


# In[ ]:


import pandas as pd

y_train_df = pd.DataFrame()
y_train_df['label'] = y_train
ax = y_train_df['label'].value_counts().plot(kind='barh', figsize = (10,10), title='Number of Samples per Class')
ax.set_yticklabels(list(map(lambda x: labels_dict[x], y_train_df['label'].value_counts().index.tolist())))            
for i, v in enumerate(y_train_df['label'].value_counts()):
    ax.text(v + 10, i - 0.25, str(v), color='black')


# ----
# 
# ## Step 2: Design and Test a Model Architecture
# 
# Design and implement a deep learning model that learns to recognize traffic signs. Train and test your model on the [German Traffic Sign Dataset](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset).
# 
# The LeNet-5 implementation shown in the [classroom](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) at the end of the CNN lesson is a solid starting point. You'll have to change the number of classes and possibly the preprocessing, but aside from that it's plug and play! 
# 
# With the LeNet-5 solution from the lecture, you should expect a validation set accuracy of about 0.89. To meet specifications, the validation set accuracy will need to be at least 0.93. It is possible to get an even higher accuracy, but 0.93 is the minimum for a successful project submission. 
# 
# There are various aspects to consider when thinking about this problem:
# 
# - Neural network architecture (is the network over or underfitting?)
# - Play around preprocessing techniques (normalization, rgb to grayscale, etc)
# - Number of examples per label (some have more than others).
# - Generate fake data.
# 
# Here is an example of a [published baseline model on this problem](http://yann.lecun.com/exdb/publis/pdf/sermanet-ijcnn-11.pdf). It's not required to be familiar with the approach used in the paper but, it's good practice to try to read papers like these.

# ### Pre-process the Data Set (normalization, grayscale, etc.)

# Minimally, the image data should be normalized so that the data has mean zero and equal variance. For image data, `(pixel - 128)/ 128` is a quick way to approximately normalize the data and can be used in this project. 
# 
# Other pre-processing steps are optional. You can try different techniques to see if it improves performance. 
# 
# Use the code cell (or multiple code cells, if necessary) to implement the first step of your project.

# **My approach:**
# - normalization will be handled within the network
# - data augmentation will include grayscaling and affine transformations

# #### Normalization

# In[3]:


from tqdm import tqdm
from skimage import exposure

### Histogram Equilization
def normalize(image_data):
    norm = np.array([exposure.equalize_adapthist(image, clip_limit=0.03) for image in tqdm(image_data)])
    return norm

print('Normalizing Training Images...')
X_train_norm = normalize(X_train)

print('Normalizing Validation Images...')
X_valid_norm = normalize(X_valid)

print('\nNormalizing Test Images...')
X_test_norm = normalize(X_test)
    


# #### Data Augmentation

# In[4]:


import keras
from keras.preprocessing.image import ImageDataGenerator

datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=8,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    fill_mode='nearest',
    horizontal_flip=False,
    vertical_flip=False
)


# In[5]:


from sklearn.utils import shuffle

max_images_per_class = 4000
X_train_aug = np.empty((0, 32, 32, 3))
y_train_aug = np.empty(0, dtype='uint8')

print('Augmenting Image Data...')
for i in tqdm(range(n_labels)):
    index = [y_train==i]
    i_class_images = X_train_norm[y_train==i]
    i_class_y = y_train[y_train==i]

    i_X_train_aug = np.copy(i_class_images)
    i_y_train_aug = np.copy(i_class_y)

    for X,y in datagen.flow(i_class_images, i_class_y, batch_size=len(i_class_y), seed=113+i*17):            
        i_X_train_aug = np.append(i_X_train_aug, X, axis=0)
        i_y_train_aug = np.append(i_y_train_aug, y, axis=0)

        if len(i_X_train_aug) >= max_images_per_class:
            break

    X_train_aug = np.append(X_train_aug, i_X_train_aug[:max_images_per_class], axis=0)
    y_train_aug = np.append(y_train_aug, i_y_train_aug[:max_images_per_class], axis=0)              


X_train_aug, y_train_aug = shuffle(X_train_aug, y_train_aug, random_state=113)

print('Augmenting Complete.')



# In[6]:


print('X_train_augmented shape: ', X_train_aug.shape)


# In[ ]:


## Show random image and label index

import random
import matplotlib.pyplot as plt 

# Show visualizations in the notebook
get_ipython().magic('matplotlib inline')

index = random.randint(0, len(X_train_aug))
image = X_train_aug[index].squeeze()

plt.figure(figsize=(1,1))
plt.imshow(image, cmap="gray")
print('label index: ', y_train_aug[index])


# In[ ]:


# Create image dictionary {label:images}

train_images_dict = dict()

for i, (image, label) in enumerate(zip(X_train_aug, y_train_aug)):
    if label not in train_images_dict:
        train_images_dict[label] = []
    train_images_dict[label].append(image)


# In[ ]:


# Verify that number of images in dict is correct
sum(len(v) for v in train_images_dict.values())


# In[ ]:


# images_labels = list(all_images.keys())
# for image_key in images_labels:        
#     subplots = 12
#     fig, axes = plt.subplots(1,subplots)
#     images_total = len(all_images[image_key])
#     print(images_total)
#     offset = images_total // subplots
#     images = [all_images[image_key][j*offset] for j in range(subplots)]
#     for i, (image, ax) in enumerate(zip(images, axes)):
#         ax.set_title(image_key)
#         ax.imshow(image.squeeze())
#     plt.tight_layout()
#     plt.subplots_adjust(top=0.85)
#     plt.show()

# all_images.clear()

import matplotlib
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)

images_labels = list(train_images_dict.keys())
for image_key in images_labels:        
    subplots = 12
    fig, axes = plt.subplots(1,subplots)
    images_total = len(train_images_dict[image_key])
    print(images_total)
    offset = images_total // subplots
    images = [train_images_dict[image_key][j*offset] for j in range(subplots)]
    for i, (image, ax) in enumerate(zip(images, axes)):
        ax.set_title(image_key)
        ax.imshow(image.squeeze())
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()

train_images_dict.clear()


# ### Model Architecture

# In[81]:


## global variables

IS_TRAIN_PHASE = 1

OUT_DIR = ".outdir"
LOG_DIR = OUT_DIR + "/logs"
MODEL_DIR = OUT_DIR + "/models"

EPOCHS = 20
BATCH_SIZE = 128

lr = 0.001      # learning rate
decay= 0.0005   # for L2 reg
keep_prob = 0.5 # for dropout
mu = 0          # normalized mean
sigma = 0.1     # normalized stdev


# #### Operations

# The series of functions below are designed to make the model more modular. This reduces the amount of hard-coding and makes it much easier to experiment with different model architectures.

# In[8]:


# applies batch normalization
def batch_norm(input, name="bn"):
    with tf.name_scope(name):
        bn = tf.nn.batch_normalization(input, mean=mu, variance=sigma, offset=None, scale=None, 
                                       variance_epsilon=1e-5, name=name)
        return bn
    

    
# applies max pooling
def max_pool(input, kernel_size=(1,1), strides=[1,1,1,1], name="maxpool"):
    H = kernel_size[0]
    W = kernel_size[1]
    
    with tf.name_scope(name):    
        pool = tf.nn.max_pool(input, ksize=[1, H, W, 1], strides=strides, padding='VALID', name=name)
        return pool


# applies dropout
def dropout(input, keep=0.9, name="drop"):
    with tf.name_scope(name):    
#         drop = tf.cond(IS_TRAIN_PHASE,
#                        lambda: tf.nn.dropout(input, keep),
#                        lambda: tf.nn.dropout(input, 1.0)
#                       )
        if IS_TRAIN_PHASE:
            drop = tf.nn.dropout(input, keep)
        else:
            drop = tf.nn.dropout(input, 1.0)
        return drop



# In[18]:


# creates convolutional layer
def conv_layer(input, n_kernels=1, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="conv"):
    H, W = kernel_size                  # filter height, width
    C = input.get_shape().as_list()[3]  # input depth
    K = n_kernels                       # output depth
    in_shape = [H, W, C, K]
    print('{} in shape: {}'.format(name, in_shape))
    
    with tf.name_scope(name):
        w = tf.Variable(tf.truncated_normal(in_shape, mean=mu, stddev=sigma), name="weights")
        b = tf.Variable(tf.zeros(K), name="biases")
        conv = tf.nn.conv2d(input, w, strides=strides, padding='SAME')
        conv = tf.nn.bias_add(conv, b)
#         tf.summary.histogram("weights", w)
#         tf.summary.histogram("biases", b)
#         tf.summary.histogram("activations", act)
        out_shape = conv.get_shape().as_list()
        print('{} out shape: {}'.format(name, out_shape))

        return conv


# creates fully connected layer
def fc_layer(input, n_inputs, n_outputs, name="fc"):
    shape = input.get_shape().as_list()
    print('{} shape: in={} out={}'.format(name, shape[1], n_outputs))
    
    with tf.name_scope(name):    
        w = tf.Variable(tf.truncated_normal([n_inputs, n_outputs], mean=mu, stddev=sigma), name="weights")
#         b = tf.Variable(tf.constant(0.01, shape=[n_outputs]), name="biases")
        b = tf.Variable(tf.zeros(n_outputs), name="biases")
        act = tf.matmul(input, w) + b
#         act = tf.add(tf.matmul(input, w), b)
#         tf.summary.histogram("weights", w)
#         tf.summary.histogram("biases", b)
#         tf.summary.histogram("activations", act)
        return act


# #### Modified LeNet Models

# In[14]:


def LeNet_2(x):
    
    with tf.name_scope("conv_1"):
        # Input = 32x32x3. 
        conv_1 = tf.nn.relu(conv_layer(x, n_kernels=16, kernel_size=(5, 5), strides=[1, 1, 1, 1]))
        # Output = 14x14x16.
        pool_1 = max_pool(conv_1, kernel_size=(2,2), strides=[1,2,2,1])

    with tf.name_scope("conv_2"):
        # Input = 14x14x16. 
        conv_2 = tf.nn.relu(conv_layer(pool_1, n_kernels=32, kernel_size=(5, 5), strides=[1, 1, 1, 1]))
        # Output = 5x5x32.
        pool_2 = max_pool(conv_2, kernel_size=(2,2), strides=[1,2,2,1])    
     
    # Flat. Input = 5x5x32. Output = 800.
    flat = tf.contrib.layers.flatten(pool_2)  # = [batch_size, k_features]
    
    k_features = flat.get_shape().as_list()[1]
    print('k_features: ', k_features)
        
    # Fully Connected. Input = 800. Output = 512.
    with tf.name_scope("fc_1"):
        fc_1 = fc_layer(flat, n_inputs=k_features, n_outputs=512)
        fc_1 = tf.nn.relu(fc_1)
    
    # Fully Connected. Input = 512. Output = 256.
    with tf.name_scope("fc_2"):
        fc_2 = fc_layer(fc_1, n_inputs=512, n_outputs=256)
        fc_2 = tf.nn.relu(fc_2)    
    
    # Fully Connected. Input = 256. Output = 43.
    with tf.name_scope("output"):
        logits = fc_layer(fc_2, n_inputs=256, n_outputs=43)
    
        return logits


# In[75]:


def LeNet_5(x):
    
    with tf.name_scope("conv_layers"):
        conv = tf.nn.relu(conv_layer(x, n_kernels=3, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="conv_0"))  
        
        conv = tf.nn.relu(conv_layer(conv, n_kernels=8, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_1"))  
        conv = tf.nn.relu(conv_layer(conv, n_kernels=16, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_2"))   
        conv = max_pool(conv, kernel_size=(2,2), strides=[1,2,2,1])    

        conv = tf.nn.relu(conv_layer(conv, n_kernels=16, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_3"))  
        conv = tf.nn.relu(conv_layer(conv, n_kernels=32, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_4"))   
        conv = max_pool(conv, kernel_size=(2,2), strides=[1,2,2,1])  

        conv = tf.nn.relu(conv_layer(conv, n_kernels=32, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_5"))  
        conv = tf.nn.relu(conv_layer(conv, n_kernels=64, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="conv_6"))   
        conv = max_pool(conv, kernel_size=(2,2), strides=[1,2,2,1])          
        
    flat = tf.contrib.layers.flatten(conv)  #  =[batch_size, k_features]  
    k_features = flat.get_shape().as_list()[1]
    print('k_features: ', k_features)
        
    with tf.name_scope("fc_layers"):
        fc = fc_layer(flat, n_inputs=k_features, n_outputs=1024, name="fc_1")
        fc = tf.nn.relu(fc)
        fc = tf.nn.dropout(fc, keep_prob)
    
        fc = fc_layer(fc, n_inputs=1024, n_outputs=512, name="fc_2")
        fc = tf.nn.relu(fc)    
        fc = tf.nn.dropout(fc, keep_prob)
    
        logits = fc_layer(fc, n_inputs=512, n_outputs=43, name="output")
    
        return logits


# In[67]:


# Inception Model 1

def inception_3(x):
    
    # Convolutional layers
    with tf.name_scope("conv_inception"):    
        # 1x1 Conv. image (32x32x3) --> 1x1 (32x32x32)  
        conv_1 = conv_layer(x, n_kernels=8, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="1x1x3x16")
        
        # 3x3 Conv. image (32x32x3) --> 1x1 (32x32x16) --> 3x3 (16x16x32) 
        conv_2a = tf.nn.relu(conv_layer(x, n_kernels=3, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="1x1x3x8"))
        conv_2b = conv_layer(conv_2a, n_kernels=8, kernel_size=(3, 3), strides=[1, 1, 1, 1], name="3x3x8x16")
#         conv_2b = tf.nn.max_pool(conv_2b, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME', name="maxpool_1")        
        
        # 5x5 Conv. image (32x32x3) --> 1x1 (32x32x16) --> 5x5 (16x16x32) 
        conv_3a = tf.nn.relu(conv_layer(x, n_kernels=3, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="1x1x3x8"))
        conv_3b = conv_layer(conv_3a, n_kernels=8, kernel_size=(5, 5), strides=[1, 1, 1, 1], name="5x5x8x16")
#         conv_3b = tf.nn.max_pool(conv_3b, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME', name="maxpool_2")        
        
        # Avg Pooling. image (32x32x3) --> 3x3 avgpool --> 1x1 (32x32x32)  
        conv_4a = tf.nn.avg_pool(x, ksize=[1,3,3,1], strides=[1,1,1,1], padding='SAME', name="3x3_avgpool")
        conv_4b = conv_layer(conv_4a, n_kernels=8, kernel_size=(1, 1), strides=[1, 1, 1, 1], name="1x1x3x16")
        
        # Concatenate and flatten above conv layers
        concat = tf.concat([conv_1, conv_2b, conv_3b, conv_4b], axis=3)
        flat = tf.nn.relu(tf.contrib.layers.flatten(concat))   
        
        # Count output features
        k_features = flat.get_shape().as_list()[1]
        print('k_features: ', k_features)
    
    # Fully Connected layers 
    with tf.name_scope("fully_connected"):
        fc_1 = fc_layer(flat, n_inputs=k_features, n_outputs=512, name="fc_1")
        fc_1 = tf.nn.relu(fc_1)
        fc_1 = dropout(fc_1, keep=keep_prob)

        fc_2 = fc_layer(fc_1, n_inputs=512, n_outputs=512, name="fc_2")
        fc_2 = tf.nn.relu(fc_2)
        fc_2 = dropout(fc_2, keep=keep_prob)
        
        logits = fc_layer(fc_2, n_inputs=512, n_outputs=43, name="output")
    
        return logits


# ### Train, Validate and Test the Model

# A validation set can be used to assess how well the model is performing. A low accuracy on the training and validation
# sets imply underfitting. A high accuracy on the training set but low accuracy on the validation set implies overfitting.

# #### Loss Functions

# In[78]:


# L2 regularization
def l2_reg(decay):
    train_vars = tf.trainable_variables() 
    with tf.name_scope("L2"):
        l2 = tf.add_n([tf.nn.l2_loss(v) for v in train_vars if 'weight' in v.name]) * decay
        return l2


# cross entropy
def cross_entropy(logits, one_hot_y):
    with tf.name_scope("xent"):
        xent = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=one_hot_y))
        tf.summary.scalar("xent", xent)
        return xent

    
# training
def train_step(lr, xent):
    with tf.name_scope("train"):
        train_step = tf.train.AdamOptimizer(learning_rate=lr).minimize(xent + l2)
        return train_step

    
# accuracy
def accuracy(logits, one_hot_y):
    with tf.name_scope("accuracy"):
        pred = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
        acc = tf.reduce_mean(tf.cast(pred, tf.float32))
        tf.summary.scalar("accuracy", acc)
        return acc


# In[61]:


def evaluate(x_data, y_data):
    num_examples = len(x_data)
    total_acc = 0
    sess = tf.get_default_session()
    for offset in range(0, num_examples, BATCH_SIZE):
        batch_x, batch_y = x_data[offset:offset+BATCH_SIZE], y_data[offset:offset+BATCH_SIZE]
        batch_acc = sess.run(acc, feed_dict={x: batch_x, y: batch_y})
#         summ = tf.summary.merge_all()
        total_acc += (batch_acc * len(batch_x))
    final_acc = total_acc / num_examples
    return final_acc


# In[82]:


# construct the graph 
import tensorflow as tf

tf.reset_default_graph()

x = tf.placeholder(tf.float32, (None, 32, 32, 3))
y = tf.placeholder(tf.int32, (None))
one_hot_y = tf.one_hot(y, 43)

logits = LeNet_5(x)      # inception_3(x) # LeNet_2(x)
l2 = l2_reg(decay)
xent = cross_entropy(logits, one_hot_y)
train = train_step(lr, xent)
acc = accuracy(logits, one_hot_y)


# In[ ]:





# In[83]:


# train on AUGMENTED image set

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())  # , feed_dict = {IS_TRAIN_PHASE : True }
    writer = tf.summary.FileWriter(LOG_DIR, graph=tf.get_default_graph())
    saver = tf.train.Saver()
    num_examples = len(X_train_aug)

    print("Training...\n--------")
    for i in range(EPOCHS):
#         X_train_aug, y_train_aug = shuffle(X_train_aug, y_train_aug)
        step = 0
        for offset in range(0, num_examples, BATCH_SIZE):
            step += 1
            start = offset
            end = offset + BATCH_SIZE
            batch_x, batch_y = X_train_aug[start:end], y_train_aug[start:end]
            sess.run(train, feed_dict={x: batch_x, y: batch_y})
            if step % 400 == 0:
                batch_acc = sess.run(acc, feed_dict={x: batch_x, y: batch_y})
                print("Epoch {}, Step {}".format(i+1, step))
                print("Training Accuracy = {:.3f}\n".format(batch_acc))
        valid_accuracy = evaluate(X_valid_norm, y_valid)
        print("Validation Accuracy = {:.3f}\n".format(valid_accuracy))
        print("--------")
    saver.save(sess, MODEL_DIR)
    print("Model saved")
    


# In[ ]:





# In[ ]:


# train on NORMALIZED image set

from sklearn.utils import shuffle

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())  # , feed_dict = {IS_TRAIN_PHASE : True }
    writer = tf.summary.FileWriter(LOG_DIR, graph=tf.get_default_graph())
    saver = tf.train.Saver()
    num_examples = len(X_train_norm)

    print("Training...\n--------")
    for i in range(EPOCHS):
        X_train_norm, y_train = shuffle(X_train_norm, y_train)
        step = 0
        for offset in range(0, num_examples, BATCH_SIZE):
            step += 1
            start = offset
            end = offset + BATCH_SIZE
            batch_x, batch_y = X_train_norm[start:end], y_train[start:end]
            sess.run(train, feed_dict={x: batch_x, y: batch_y})
            if step % 100 == 0:
                batch_acc = sess.run(acc, feed_dict={x: batch_x, y: batch_y})
                print("Epoch {}, Step {}".format(i+1, step))
                print("Training Accuracy = {:.3f}\n".format(batch_acc))
        valid_accuracy = evaluate(X_valid_norm, y_valid)
        print("Validation Accuracy = {:.3f}\n".format(valid_accuracy))
        print("--------")
    saver.save(sess, MODEL_DIR)
    print("Model saved")
    


# In[ ]:





# In[ ]:


# train on STANDARD image set

from sklearn.utils import shuffle

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())  # , feed_dict = {IS_TRAIN_PHASE : True }
    writer = tf.summary.FileWriter(LOG_DIR, graph=tf.get_default_graph())
    saver = tf.train.Saver()
    num_examples = len(X_train)

    print("Training...\n--------")
    for i in range(EPOCHS):
        X_train, y_train = shuffle(X_train, y_train)
        step = 0
        for offset in range(0, num_examples, BATCH_SIZE):
            step += 1
            start = offset
            end = offset + BATCH_SIZE
            batch_x, batch_y = X_train[start:end], y_train[start:end]
            sess.run(train, feed_dict={x: batch_x, y: batch_y})
            if step % 100 == 0:
                batch_acc = sess.run(acc, feed_dict={x: batch_x, y: batch_y})
                print("Epoch {}, Step {}".format(i+1, step))
                print("Training Accuracy = {:.3f}\n".format(batch_acc))
        valid_accuracy = evaluate(X_valid, y_valid)
        print("Validation Accuracy = {:.3f}\n".format(valid_accuracy))
        print("--------")
    saver.save(sess, MODEL_DIR)
    print("Model saved")
    


# In[ ]:





# In[ ]:





# In[ ]:





# ---
# 
# ## Step 3: Test a Model on New Images
# 
# To give yourself more insight into how your model is working, download at least five pictures of German traffic signs from the web and use your model to predict the traffic sign type.
# 
# You may find `signnames.csv` useful as it contains mappings from the class id (integer) to the actual sign name.

# ### Load and Output the Images

# In[ ]:


### Load the images and plot them here.
### Feel free to use as many code cells as needed.


# ### Predict the Sign Type for Each Image

# In[ ]:


### Run the predictions here and use the model to output the prediction for each image.
### Make sure to pre-process the images with the same pre-processing pipeline used earlier.
### Feel free to use as many code cells as needed.


# ### Analyze Performance

# In[ ]:


### Calculate the accuracy for these 5 new images. 
### For example, if the model predicted 1 out of 5 signs correctly, it's 20% accurate on these new images.


# ### Output Top 5 Softmax Probabilities For Each Image Found on the Web

# For each of the new images, print out the model's softmax probabilities to show the **certainty** of the model's predictions (limit the output to the top 5 probabilities for each image). [`tf.nn.top_k`](https://www.tensorflow.org/versions/r0.12/api_docs/python/nn.html#top_k) could prove helpful here. 
# 
# The example below demonstrates how tf.nn.top_k can be used to find the top k predictions for each image.
# 
# `tf.nn.top_k` will return the values and indices (class ids) of the top k predictions. So if k=3, for each sign, it'll return the 3 largest probabilities (out of a possible 43) and the correspoding class ids.
# 
# Take this numpy array as an example. The values in the array represent predictions. The array contains softmax probabilities for five candidate images with six possible classes. `tk.nn.top_k` is used to choose the three classes with the highest probability:
# 
# ```
# # (5, 6) array
# a = np.array([[ 0.24879643,  0.07032244,  0.12641572,  0.34763842,  0.07893497,
#          0.12789202],
#        [ 0.28086119,  0.27569815,  0.08594638,  0.0178669 ,  0.18063401,
#          0.15899337],
#        [ 0.26076848,  0.23664738,  0.08020603,  0.07001922,  0.1134371 ,
#          0.23892179],
#        [ 0.11943333,  0.29198961,  0.02605103,  0.26234032,  0.1351348 ,
#          0.16505091],
#        [ 0.09561176,  0.34396535,  0.0643941 ,  0.16240774,  0.24206137,
#          0.09155967]])
# ```
# 
# Running it through `sess.run(tf.nn.top_k(tf.constant(a), k=3))` produces:
# 
# ```
# TopKV2(values=array([[ 0.34763842,  0.24879643,  0.12789202],
#        [ 0.28086119,  0.27569815,  0.18063401],
#        [ 0.26076848,  0.23892179,  0.23664738],
#        [ 0.29198961,  0.26234032,  0.16505091],
#        [ 0.34396535,  0.24206137,  0.16240774]]), indices=array([[3, 0, 5],
#        [0, 1, 4],
#        [0, 5, 1],
#        [1, 3, 5],
#        [1, 4, 3]], dtype=int32))
# ```
# 
# Looking just at the first row we get `[ 0.34763842,  0.24879643,  0.12789202]`, you can confirm these are the 3 largest probabilities in `a`. You'll also notice `[3, 0, 5]` are the corresponding indices.

# In[ ]:


### Print out the top five softmax probabilities for the predictions on the German traffic sign images found on the web. 
### Feel free to use as many code cells as needed.


# ### Project Writeup
# 
# Once you have completed the code implementation, document your results in a project writeup using this [template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) as a guide. The writeup can be in a markdown or pdf file. 

# > **Note**: Once you have completed all of the code implementations and successfully answered each question above, you may finalize your work by exporting the iPython Notebook as an HTML document. You can do this by using the menu above and navigating to  \n",
#     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission.

# ---
# 
# ## Step 4 (Optional): Visualize the Neural Network's State with Test Images
# 
#  This Section is not required to complete but acts as an additional excersise for understaning the output of a neural network's weights. While neural networks can be a great learning device they are often referred to as a black box. We can understand what the weights of a neural network look like better by plotting their feature maps. After successfully training your neural network you can see what it's feature maps look like by plotting the output of the network's weight layers in response to a test stimuli image. From these plotted feature maps, it's possible to see what characteristics of an image the network finds interesting. For a sign, maybe the inner network feature maps react with high activation to the sign's boundary outline or to the contrast in the sign's painted symbol.
# 
#  Provided for you below is the function code that allows you to get the visualization output of any tensorflow weight layer you want. The inputs to the function should be a stimuli image, one used during training or a new one you provided, and then the tensorflow variable name that represents the layer's state during the training process, for instance if you wanted to see what the [LeNet lab's](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) feature maps looked like for it's second convolutional layer you could enter conv2 as the tf_activation variable.
# 
# For an example of what feature map outputs look like, check out NVIDIA's results in their paper [End-to-End Deep Learning for Self-Driving Cars](https://devblogs.nvidia.com/parallelforall/deep-learning-self-driving-cars/) in the section Visualization of internal CNN State. NVIDIA was able to show that their network's inner weights had high activations to road boundary lines by comparing feature maps from an image with a clear path to one without. Try experimenting with a similar test to show that your trained network's weights are looking for interesting features, whether it's looking at differences in feature maps from images with or without a sign, or even what feature maps look like in a trained network vs a completely untrained one on the same sign image.
# 
# <figure>
#  <img src="visualize_cnn.png" width="380" alt="Combined Image" />
#  <figcaption>
#  <p></p> 
#  <p style="text-align: center;"> Your output should look something like this (above)</p> 
#  </figcaption>
# </figure>
#  <p></p> 
# 

# In[ ]:


### Visualize your network's feature maps here.
### Feel free to use as many code cells as needed.

# image_input: the test image being fed into the network to produce the feature maps
# tf_activation: should be a tf variable name used during your training procedure that represents the calculated state of a specific weight layer
# activation_min/max: can be used to view the activation contrast in more detail, by default matplot sets min and max to the actual min and max values of the output
# plt_num: used to plot out multiple different weight feature map sets on the same block, just extend the plt number for each new feature map entry

def outputFeatureMap(image_input, tf_activation, activation_min=-1, activation_max=-1 ,plt_num=1):
    # Here make sure to preprocess your image_input in a way your network expects
    # with size, normalization, ect if needed
    # image_input =
    # Note: x should be the same name as your network's tensorflow data placeholder variable
    # If you get an error tf_activation is not defined it may be having trouble accessing the variable from inside a function
    activation = tf_activation.eval(session=sess,feed_dict={x : image_input})
    featuremaps = activation.shape[3]
    plt.figure(plt_num, figsize=(15,15))
    for featuremap in range(featuremaps):
        plt.subplot(6,8, featuremap+1) # sets the number of feature maps to show on each row and column
        plt.title('FeatureMap ' + str(featuremap)) # displays the feature map number
        if activation_min != -1 & activation_max != -1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin =activation_min, vmax=activation_max, cmap="gray")
        elif activation_max != -1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmax=activation_max, cmap="gray")
        elif activation_min !=-1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin=activation_min, cmap="gray")
        else:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", cmap="gray")

