<<<<<<< HEAD

# 程序说明

## 运行环境
Linux 或 Mac OS均可。由于使用了一点shell脚本，所以对Windows不支持。但需要时，可以修改。
	
## 安装
1. 安装Python 2.7.6(2.7.11亦可), <https://www.python.org/downloads/>

2. 安装结巴分词, <https://github.com/fxsjy/jieba>
  
3. 安装 boost program-options (Vowpal Wabbit用到)

   对于Redhat系Linux(CentOS)
   ```
   yum install boost-devel
   ```
   
   对Ubuntu/Debian/Mint
   ```
   apt-get install libboost-program-options-dev
   ```
   
3. 安装Vowpal Wabbit, <https://github.com/JohnLangford/vowpal_wabbit>

4. 设置vw可执行程序的环境变量
    vw通常在vowpal wabbit项目的vowpalwabbit目录下。例如：
    
	```
	export VW=/root/work/dl/vowpal_wabbit.8.1.1/vowpalwabbit/vw
	```

## 使用

### 准备数据

如果已经有数据，将测试集和训练集拷贝trian.txt, test.txt拷贝到data目录下。ln -s 建立符号链接亦可。
如果没有，可从此[链接](http://pan.baidu.com/s/1bom8Ry3)下载, 密码: rx93 

### Feature 转换

训练集
```
python code/convert_feats_seg.py data/train.txt data/train.seg.cnt.vw
```
测试集，需要加开关 -t
```
python code/convert_feats_seg.py data/test.txt data/test.seg.cnt.vw -t
```

### 随机划分测试集

```
python code/split_folds.py data/train.seg.cnt.vw  -n 5 --seed 12345
```

### Grid Search

编辑 code/grid_search_vw.py文件。可修改的参数有：
* ngram
* skips
* learning_rate: 学习率
* l1: L1调整
* l2: L2调整
* passes: 
* decay_learning_rate
* threshold:  预测概率转换为label(0/1)的阈值

目前代码中保留的，都是最优参数组合。可以任意修改成其它参数，进行试验。

### 训练最优模型并提交

修改shell中的vowpal wabbit参数，执行shell并提交。

```
./mksub_vw.sh
```

=======
# ccf2015-sms-spam
>>>>>>> 599d62e6963bcd8ace8a7b3f71350b84af5e2543
