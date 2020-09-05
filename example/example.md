
# 第 5 章 卷积神经网络

## 引言

- Q:卷积神经网络的3个**结构**上的特性是什么？
是什么呢？(测试块内多行)
    - *斜体特性*试试看，==高亮==特性玩一下，权重共享
    - $$y_{i j}=\sum_{u, v} w_{u v} x_{i+u-1, j+v-1}$$
    - ![](http://anki190912.xuexihaike.com/20200903210016.png?imageView2/2/h/150)

## 5.1 卷积

- Q:最长不下降子序列的`实现代码`？(代码块测试)
    - ```c++

      #include <cstdio>
      int main() {
          return 0;
      }
      ```


- Q:卷积的导数是什么？假设$\boldsymbol{Y}=\boldsymbol{W} \otimes \boldsymbol{X}$，其中$\boldsymbol{X} \in \mathbb{R}^{M \times N}, \boldsymbol{W} \in \mathbb{R}^{U \times V}, \boldsymbol{Y} \in \mathbb{R}^{(M-U+1) \times(N-V+1)},$，函数$f(\boldsymbol{Y}) \in \mathbb{R}$为一个标量函数，则$\frac{\partial f(\boldsymbol{Y})}{\partial w_{u v}}$是什么？
    - $$\begin{aligned}
\frac{\partial f(\boldsymbol{Y})}{\partial w_{u v}} &=\sum_{i=1}^{M-U+1} \sum_{j=1}^{N-V+1} \frac{\partial y_{i j}}{\partial w_{u v}} \frac{\partial f(\boldsymbol{Y})}{\partial y_{i j}} \\
&=\sum_{i=1}^{M-U+1} \sum_{j=1}^{N-V+1} \frac{\partial f(\boldsymbol{Y})}{\partial y_{i j}} x_{u+i-1, v+j-1}
\end{aligned}$$
    - 从上式可知，$f(\boldsymbol{Y})$关于$\boldsymbol{W}$的偏导数为$\boldsymbol{X}$和$\frac{\partial f(\boldsymbol{Y})}{\partial \boldsymbol{Y}}$的卷积，即
