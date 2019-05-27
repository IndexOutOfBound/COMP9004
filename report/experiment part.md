
## Experiment

In this part, We are going to figure out how each variable can influence the tendency of gini index.

### Pre-analyzing

Before we run the detaild experiment of our model, we try to choose a set of hyperparameters to make the gini index change linearly. We create two index to explain the transformation of variables.

$$Resource = \frac {\text {num grain grown}}{\text{grain grow interval}} * \text{percent best land} $$

The value of $Resource$ represent the richness of resource.  The bigger the $Resource$, the easier for people to get grains.
$$Talent = \frac {\text{max vision}}{\text{metabolism max}}$$
The value of $Talent$ represent the ability of a people, The bigger the value, the stronger the individual.

### Executing

According to the analysis above, we adjust the variables to increase the $Resource$ at first and then the $Talent$. Then we got 77 groups of parameters.

ID|num grain grown | grain grow interval | percent best land | max vision | metabolism max
--|--|--|--|--|--
1|1|10|5%|1|25|
||...|
10|10|10|5%|1|25|
|||...
19|10|1|5%|1|25|
||||...
39|10|1|25%|1|25
|||||...
53|10|1|25%|15|25
||||||...
77|10|1|25%|15|1

Each group of parameters will run 10 times and each time will calculate the average of last 200 tickets' gini index. Then we will calculate the average result of 10 times as the gini index of this group of parameters.

### Analysis

We use a line chart to show the result of our model. It can easily to find that the transformation of gini index is similar to the value of $Resource/Talent$.

![](http://ww3.sinaimg.cn/large/006tNc79ly1g3fni8qg0xj312u0u0qda.jpg)

The curve of Gini index can be depart to five phases.

#### 1st phases: 1~13

During this phase, The total resource in the world is very limited, The mainly source of grains is from rebirth. Thus, the Gini index keeps in a low degree and increases slowly.

#### 2nd phases: 14~26

The Gini index has a remarkable growth in this phase with the total resource increase.

#### 3rd phases: 27~39

When the resource grow to a high level, the Gini index will not continue increasing, it will remain at a relatively stable level. This might be the most darkness time of the virtual world. There are sufficient resource but an extreme gap between the poor and the rich.

#### 4th phases: 40~46

This is an exciting result. It shows that even a little improvment of people's ability will obviously eliminate the wealthy gap.

#### 5th phases: 47~77

When the $Talent$ increase to a threshold, we notice that the Gini index will slowly reduce. Eventually, The Gini index will back to the same level as the very beginning.