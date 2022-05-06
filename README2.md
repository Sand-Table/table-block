# Sticker detection using Faster-RCNN 🎉 

### Bachelors project at EPFL 2021

---

## Week 1 :

* Learning how to read scientific papers, took a look at [Frustratingly Simple Few-Shot Object Detection](https://arxiv.org/pdf/2003.06957v1.pdf) 
    * The abstract of scientific papers usually states the simple but obvious
    * The intro states what the problem is and what their approach to fixing it will be. In this problem they only modify the last layer, that is the Box Classifier and the Box Regressor.

* The previous cited paper uses Detectron 2, which implements Faster-RCNN in PyTorch - **This is likely what I will be using for this project** 

* [COCO](https://cocodataset.org/#home) is a dataset frequently used in the field of object detection 

* [Paperswithcode](https://paperswithcode.com/task/few-shot-object-detection) has an excellent database of possible reseach papers with implementations.

---

## Week 2

Although **RetinaNet** is proposal free and thus faster as it is just one CNN it lacks the modularity of the proposal based **Faster-RCNN** (Which is **Fast-RCNN** with a **RPN**).

Deep object cosegmentation takes two images and finds the common features, would be potentially efficient for comparing to existing stickers.



* [Few-shot Object Detection via Feature Reweighting](https://arxiv.org/pdf/1812.01866v2.pdf) Proposal based vs Proposal free: Uses loadable vectors to change the weights, with two Inputs, Meta-feature and LW reweighting

* [Few-Shot Object Detection with Attention-RPN and Multi-Relation Detector](https://arxiv.org/pdf/1908.01998v4.pdf) No need to fine tune the model to novel classes - Uses way more catergories and few images per category, uses Attention network (Garbage in -> Garbage out). Concept of multirelation

* [Polytechnique X, MetaLearning algorithms](https://arxiv.org/pdf/1909.13579v1.pdf) Interesting paper with details of implementation

* [Mask R-CNN](https://arxiv.org/pdf/1703.06870.pdf) The reference in Proposal based FSO detection
    * [Amazing blog post on the implementation of Mask R-CNN](https://engineering.matterport.com/splash-of-color-instance-segmentation-with-mask-r-cnn-and-tensorflow-7c761e238b46)
    * [Implementation of Mask R-CNN](https://github.com/matterport/Mask_RCNN) Sadly uses tensowflow

---

## Week 3

Installed Detectron2 in myenv environment, with PyTorch 1.7.1 and TorchVision 0.8.2, CPU version. Would like to connect to SCITAS and use that instead.

D2Go is interesting optimised version of Detectron2 but for mobile phones, gotta check it out.

* [Fantastic intro to detectron2](https://www.youtube.com/watch?v=EVtMT6Ve0sY)

* [Traffic sign detection](https://www.youtube.com/watch?v=SWaYRyi0TTs) Could be useful as similar to stickers

* [How to train detectron2 on a custom dataset](https://www.youtube.com/watch?v=CrEW8AfVlKQ)
    * [The blog](https://gilberttanner.com/blog/detectron-2-object-detection-with-pytorch) Where it is explained in great detail


* Datasets:
    * [FlikrLogos](https://www.uni-augsburg.de/en/fakultaet/fai/informatik/prof/mmc/research/datensatze/flickrlogos/) Have to send email to get dataset ✔
    * [BelgaLogos](http://www-sop.inria.fr/members/Alexis.Joly/BelgaLogos/BelgaLogos.html#download)

* A [mobile first version](https://github.com/facebookresearch/d2go) of Detectron2 which is light weight

### How to run detecton2 demo:

<details close>
<summary></summary>

- Install packages from [here](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md)

- Run after pulling the git

```terminal
git clone https://github.com/facebookresearch/detectron2.git
cd demo
python demo.py --config-file ../configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml --input ../../input.jpg --opts MODEL.DEVICE cpu MODEL.WEIGHTS detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl
```
</details>


### Issues I ran into:
<details close>
<summary></summary>
- Had to add MODEL.DEVICE cpu for it to run on CPU

- Had to point to a downloaded image
```
wget http://images.cocodataset.org/val2017/000000439715.jpg -q -O input.jpg
```

- Had to install two libraries for OpenCV
```
pip install opencv
```
</details>

### What I learned

- How to do Markdown
- Why and how of Conda environments
- How to use detectron pretrained models

- Names of the pretrained

    - R50, R101 is [MSRA Residual Network](https://github.com/KaimingHe/deep-residual-networks)
    - X101 is ResNeXt
    - Use 3x as it is more trained than 1x

---

## Week 4

Managed to ssh into SCITAS, spent some time understanding how to access CUDA, got it to run!

Downloaded the FlickrLogo dataset [Links](notes/PRIVATE.md)!

Wrote a simple [script](execute.sh) that will execute as a job using Slurm, made a venv with these packages added user for it to not be system installed:

```terminal
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.7/index.html --user
pip install torch==1.7.1 torchvision==0.8.2 --user
pip install opencv-python --user
pip install -U iopath==0.1.4 --user
```

To interact with SCITAS *and* have it on the GPUs

```terminal
Sinteract -t 00:10:00 -p gpu -q gpu_free -g gpu:1
```

### Issues I ran into:
<details close>
<summary></summary>

- Have to load python after the venv as venv replaces the python version

- Have to install opencv-python everytime even I'm in the venv?
```terminal
pip install opencv-python --user
```
- Had to downgrade iopath for it to work on SCITAS
```
pip install -U iopath==0.1.4 --user
```
</details>


### What I learned:

- How to use SCITAS again :P

- How to use scp and send the images back to my local machine

- How to launch jobs instead of using Sinteract

- What Python notebooks were and there use using the [detectron2 tutorial](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5#scrollTo=8IRGo8d0qkgR)

---

## Week 5

Used FlickrLogos32 to learn to custom dataset training.

| FlickrLogos32   |      1 Class      |  32 Classes |
|:----------|:-------------:|:------:|
| L 0.007 | [link]("Flicker1Classes/L0.007_900") | [link]("Flicker32Classes/L0.007_900") |
| L 0.005 | [link]("Flicker1Classes/L0.005_2000") | [link]("Flicker32Classes/L0.005_2000") |
| L 0.001 | [link]("Flicker1Classes/L0.001_4000") | [link]("Flicker32Classes/L0.001_4000") |


Detectron needs to register a `list`\[`dict`\], a list of metadata about each image. The __dataloader__ will then augment, batch and give to `model.forward()`

### Issues I ran into:
<details close>
<summary></summary>

- How to correctly open pictures (Had an annoying "\n" that was invisible in print() but not when passing as a path to open the image)

- How to correctly pass the mask (Have to transform it into __RLE__ which is lightweight binary mask)

- That I have to load the config of the model with my custom one

- Too much memory use for the C4 models

- After making my custom dataset and running it on SCITAS, it took around ~3h to get _some_ sort of result,         obtaining 3-4% on random parts of the picture by running it through the detectron2 Visualiser class. I tried using multiple different backbones, from `C4`, `DC5`, `FPN` and `3x` or `1x` to see if it would make a difference. 

    Loss was at around `0.2` after ~15 minutes of training for an **abysmal** result. Results were slightly better for the classes version

    What solved the problem was changing the learning rate from 0.00025 to 0.02

</details>

### What I learned:

- The inner structure of detectron2, python (again)

- How to use `rsync`

- P a t i e n c e :stars:

---

## Week 5 Part 2

- Built a python bot that cuts out people from pictures that are submitted to it, you can try it out here: https://t.me/faststicker_bot

    - Hosted on heroku, took ~10h to do. Learned a lot about git, heroku and python dependencies.

- Tried out the Flicker1Class47 dataset

---

## Week 6

- Label stickers, maybe just the box to then attempt to classify them [link](https://github.com/wkentaro/labelme)

- Look around for the precision and curve, as well as IOU.

- 

---

## Week 10

Time to classify the stickers using Few Shot Image Classification. There are three pillars in this domain:

- Prior knowledge about Similarity (Knows how to differitiate well)

- Prior knowledge about Learning (Knows how to adapt well)

- Prior knowledge about the data (Augment data to learn)

Detectron2 only needs 10 images per class in the training to start recognizing logos.

I chose to go with similarity implementations, specifically Matching Networks, which are basically KNNs with extra steps.

**Lots of random research and looking at random indians on youtube**

---

## Week 11

I decided to go with [Oscar's implementation in python](https://github.com/oscarknagg/few-shot)

In which he highlights how to implement the Matching Networks in Python using PyTorch

### Issues I ran into:
<details close>
<summary></summary>

- Issue following instructions of the git repo, but after downloading the miniImageNet dataset and setting it up all good

- Had to change the pythonpath for it to have access to the local files config.py

```
export PYTHONPATH=.
```

- After uploading all the files to the SCITAS cluster, I simply created a new environment with venv and installed all the libraries (Was missing Scikit, not sure why)

- Basically roasting my computer 3 times trying to load the files of the datasets (Unzip)

- The program that I downloaded uses q queries * k classes across the k classes when I simply want to be able to ask for a single image (Instead of k ones) Because of this I had to rewrite part of the program, and manage to make it run on the SCITAS servers.

- Running the miniImageNet dataset is a pain because it is much more complex than the omniglot one. (Omniglot takes ~10min to run compared to the 2h of the miniImageNet one)

</details>

### Adding the option to run on one image:
<details close>
<summary></summary>

- Change core.py so that the NShotTaskSampler takes the first sample instead of k.

- Change core.py so that the create_nshot_task_label generates a target label of [0]

- Create tugdual.py which loads the dataset and prepares a n_shot_task with a batch so we can check 

</details>


### What I learned:

- How to read instructions :P

- Simple use of requirements.txt

- Metric Learning: Find encoding space in which classes are grouped together and far apart from one another. 
    - Original concept was with Siamese networks (CNN Enconder to get feature embeddings) and then compare using any energy function (Cosine, Euclidean distance). If below a certain threshold then the images belong to the same class.

    - Prototypical networks take it a step further by encoding the n-shots of each class into a prototype, a.k.a. the mean of the encodings. Distance function is used to calculate distance and then a softmax to obtain the probabilities of the query image belonging to a class.

- "Omniglot [16] is a dataset of 1623 handwritten characters collected from 50 alphabets. There are 20examples associated with each character, where each example is drawn by a different human subject.We follow the procedure of Vinyals et al.[29]by resizing the grayscale images to 28×28 andaugmenting the character classes with rotations in multiples of 90 degrees" - Proto. type

--- 

## Week 14

Wrote tugdual.py which is a python script to test with 1 image the Prototypical networks!

Striped the useless stuff of the classifier and added the option to run on the __CPU__ instead of the __CUDA__

I want to test if it genuinely works with a random input, so I decided to give it a random drawing 

Wrote customOmniglot.py which bypasses all the batch preprocessing and just feeds the model random images from the custom_data. Did the same with miniImageNet before adding a Dataset.py, running it on the SCITAS and downloading the model to create a customLogos.py which loads customData set. I suspect that it is clearly __overfitted__.

![](images/ArcadianCharacter01.jpg)

### Issues I ran into:
<details close>
<summary></summary>


</details>


### What I learned:

- 

---

# Works to cite:

Scalable Logo Recognition in Real-World Images
Stefan Romberg, Lluis Garcia Pueyo, Rainer Lienhart, Roelof van Zwol
ACM International Conference on Multimedia Retrieval 2011 (ICMR11), Trento, April 2011. 


Vinyals, Oriol, et al. "Matching networks for one shot learning." arXiv preprint arXiv:1606.04080 (2016).