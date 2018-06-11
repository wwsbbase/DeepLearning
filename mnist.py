# remote debug
# import ptvsd
# ptvsd.settrace(None, ('0.0.0.0', 18110))
# ptvsd.wait_for_attach()

#首先导入一些用到的库。
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from matplotlib import pyplot as plt

#%matplotlib inline
tf.logging.set_verbosity(tf.logging.INFO)

#先来看看数据长什么样子

mnist = input_data.read_data_sets("./")

print(mnist.train.images.shape)
print(mnist.train.labels.shape)

print(mnist.validation.images.shape)
print(mnist.validation.labels.shape)

print(mnist.test.images.shape)
print(mnist.test.labels.shape)


#可以看到images里面有数量不等的图片，每张图片是28x28长度的一个一维向量， 所以用的时候需要先给它还原成28x28的二维图片。
# labels中则是图片对应的数字的值。


# plt.figure(figsize=(8,8))

# for idx in range(16):
#     plt.subplot(4,4, idx+1)
#     plt.axis('off')
#     plt.title('[{}]'.format(mnist.train.labels[idx]))
#     plt.imshow(mnist.train.images[idx].reshape((28,28)))

#
#接下来，定义用于训练的网络
# 首先定义网络的输入。
# 这里我们直接使用上面的数据作为输入，所以定义两个placeholder分别用于图像和lable数据，另外，定义一个float类型的变量用于设置学习率。
# 为了让网络更高效的运行，多个数据会被组织成一个batch送入网络，两个placeholder的第一个维度就是batchsize，因为我们这里还没有确定batchsize，所以第一个维度留空。
	
# label 就是ground truth
x = tf.placeholder("float", [None, 784])
y = tf.placeholder("int64", [None])
learning_rate = tf.placeholder("float")

#
#两层网络结构图的构建

def initialize(shape, stddev=0.1):
  return tf.truncated_normal(shape, stddev=0.1)

L1_units_count = 100

W_1 = tf.Variable(initialize([784, L1_units_count], stddev=0.05))
b_1 = tf.Variable(initialize([L1_units_count]))
logits_1 = tf.matmul(x, W_1) + b_1
output_1 = tf.nn.relu(logits_1)

#第二层就是输出层，不需要激活
L2_units_count = 10 
W_2 = tf.Variable(initialize([L1_units_count, L2_units_count], stddev=0.063))
b_2 = tf.Variable(initialize([L2_units_count]))
logits_2 = tf.matmul(output_1, W_2) + b_2  

logits = logits_2

#
#接下来定义loss和用于优化网络的优化器。
# loss计算使用了sparse_softmax_cross_entropy_with_logits, 这样做的好处是labels可以不用手动做one_hot省了一些麻烦。
# 这里使用了sgd优化器，学习率为可以根据需要设定。
#tf.reduce_mean 求平均值

cross_entropy_loss = tf.reduce_mean(
    tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=y))

optimizer = tf.train.GradientDescentOptimizer(
    learning_rate=learning_rate).minimize(cross_entropy_loss)

# 需要注意的是，上面的网络，最后输出的是未经softmax的原始logits，而不是概率分布， 要想看到概率分布，还需要做一下softmax。

# 将输出的结果与正确结果进行对比，即可得到我们的网络输出结果的准确率。
	
pred = tf.nn.softmax(logits)
correct_pred = tf.equal(tf.argmax(pred, 1), y)
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# saver用于保存或恢复训练的模型。

batch_size = 32
trainig_step = 1000

saver = tf.train.Saver()


# 以上定义的所有操作，均为计算图，也就是仅仅是定义了网络的结构，实际需要运行的话，还需要创建一个session，并将数据填入网络中。

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    #定义验证集与测试集
    validate_data = {
        x: mnist.validation.images,
        y: mnist.validation.labels,
    }
    test_data = {x: mnist.test.images, y: mnist.test.labels}

    for i in range(trainig_step):
        xs, ys = mnist.train.next_batch(batch_size)
        _, loss = sess.run(
            [optimizer, cross_entropy_loss],
            feed_dict={
                x: xs,
                y: ys,
                learning_rate: 0.3
            })

        #每100次训练打印一次损失值与验证准确率
        if i > 0 and i % 100 == 0:
            validate_accuracy = sess.run(accuracy, feed_dict=validate_data)
            print(
                "after %d training steps, the loss is %g, the validation accuracy is %g"
                % (i, loss, validate_accuracy))
            saver.save(sess, './model.ckpt', global_step=i)

    print("the training is finish!")
    #最终的测试准确率
    acc = sess.run(accuracy, feed_dict=test_data)
    print("the test accuarcy is:", acc)

if validate_accuracy >=0.98:
    score = 100
elif validate_accuracy >=0.96 and validate_accuracy <0.98 :
    score = 60
else:
    score = 0
print('#'*10)
print('Your final score:[{}]'.format(score))
print('#'*10)



