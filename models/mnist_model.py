import tensorflow as tf
import numpy as np
import os


def Linear_Softmax_GradientDescentOptimizer(data, sess, x, y_, keep_prob, iter=1000, restore=0):
    """
    a gradient descent optimizer
    :param data: dataset
    :param sess: tensorflow session
    :param x: tensorflow placeholder for training data
    :param y_: tensorflow placeholder for training label
    :param keep_prob: drop out probability
    :param iter: iteration time for training
    :return: y: target function / predicted value
    """
    # target function
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    sess.run(tf.global_variables_initializer())
    y = tf.matmul(x, W) + b

    # loss function or cost function
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    # steepest gradient descent
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    if not restore:
        for _ in range(iter):
            batch = data.train.next_batch(100)
            sess.run(train_step, feed_dict={x: batch[0], y_: batch[1]})
    else:
        saver = tf.train.Saver()
        save_path = ".%scheckpoint%sLinear_Softmax_GradientDescentOptimizer.ckpt" % (os.sep, os.sep)
        saver.restore(sess, save_path)
        print("[+] Model restored")

    return tf.nn.softmax(y), cross_entropy


def ReLU_Softmax_AdamOptimizer(data, sess, x, y_, keep_prob, train_iter=20000, restore=False):
    """A small convolutional neural network for MNIST.
    
    The exact same network structure as the TensorFlow tutorial for MNIST
    
    Parameters
    ----------
    data : dataset, 'MNIST_data'
        the MNIST dataset
    sess : session
        the TensorFlow session
    x : placeholder
        the TensorFlow placeholder for the input of MNIST dataset
    y_ : placeholder
        the TensorFlow placeholder for the correct label of the corresponding input data
    keep_prob : placeholder
        the TensorFlow placeholder for the keep probability of drop out
    train_iter : int, 20000
        the number of iteration used to train the DNNs
    restore : Boolean, False
        the flag indicates to train a new network or restore from the checkpoint.
    
    Returns
    -------
    y_conv_softmax : tensor
        the TensorFlow tensor represents the predicted value inferred by the DNNs
    cross_entropy : tensor
        the TensorFlow tensor represents the cost function used by the DNNs    
    """

    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # First Convolutional Layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # Second Convolutional Layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # Densely Connected Layer
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout in order to avoid overfitting
    # keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Readout Layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    # similar cost function as Gradient Descent Optimizer which is cross_entropy
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    # evaluate the model for each training step
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    if not restore:
        sess.run(tf.global_variables_initializer())
        # start training
        for i in range(train_iter):
            batch = data.train.next_batch(50)
            if i % 100 == 0:
                train_accuracy = sess.run(accuracy, feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
                print("step %d, training accuracy %g" % (i, train_accuracy))
            sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    else:
        saver = tf.train.Saver()
        save_path = ".%scheckpoint%s%s.ckpt" % (os.sep, os.sep, "mnist_DNNs")
        saver.restore(sess, save_path)
        print("[+] Model restored")

    y_conv_softmax = tf.nn.softmax(y_conv)
    return y_conv_softmax, cross_entropy


def ReLU_Softmax_AdTraining(data, sess, x, y_, keep_prob, iter=20000, restore=0):
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # First Convolutional Layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # Second Convolutional Layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # Densely Connected Layer
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout in order to avoid overfitting
    # keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Readout Layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    cross_entropy_old = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

    # the code before is the same as ReLU_Softmax_AdamOptimizer
    # the code below will be adding regularization to the lost function which is the main difference
    # TODO: confused about how to maintain same theta for x and x_adversarial
    alpha = 1
    # epsilon = 0.25
    # nabla_J = tf.gradients(cross_entropy_old, x)
    # sign_nabla_J = tf.sign(nabla_J)
    # eta = tf.multiply(sign_nabla_J, epsilon)
    # eta_flatten = tf.reshape(eta, [-1, 784])
    # x_adversarial = tf.add(x,eta_flatten)

    # adding regularization
    cross_entropy = tf.multiply(cross_entropy_old, alpha)

    # the code below is the same as ReLU_Softmax_AdamOptimizer
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    if not restore:
        sess.run(tf.global_variables_initializer())
        # start training
        for i in range(iter):
            batch = data.train.next_batch(50)
            if i % 100 == 0:
                train_accuracy = sess.run(accuracy, feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
                print("step %d, training accuracy %g" % (i, train_accuracy))
            sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    else:
        saver = tf.train.Saver()
        save_path = ".%scheckpoint%sReLU_Softmax_AdTraining.ckpt" % (os.sep, os.sep)
        saver.restore(sess, save_path)
        print("[+] Model restored")

    return tf.nn.softmax(y_conv), cross_entropy
