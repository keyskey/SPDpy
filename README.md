# SPD
Multi agent simulation code of Spatial Prisoner's Dilemma(SPD) Game on a complex network.<br>

<img src="https://user-images.githubusercontent.com/39644776/41784084-9bb5b1b4-7679-11e8-87be-2401128dd9a6.png" width="400px" title="Image of the game on lattice"> <br>
(C: Cooperator, D: Defector) <br>

## Requierements:<br>
You need to install Python3 with <a href="https://www.anaconda.com/"> Anaconda</a> distribution.

When running the simulation, just type <br>
$ python SPD.py <br>
on your terminal. You can visualize the result with heatmap.py.<br>
$ python heatmap.py <br>
<br>
Depending on the topology and strategy update rule, you can see various Dg-Dr diagram.<br>
<br>

|Imitation max strategy update on lattice|Pairwise-Fermi strategy update on BA-Scale Free network|
|:---:|:---:|
|<img src="https://user-images.githubusercontent.com/39644776/41786084-79b1138c-767f-11e8-9316-b81229a3dcdf.png" width="400px">|<img src="https://user-images.githubusercontent.com/39644776/41786092-7e3ee1d6-767f-11e8-95c3-6523d7392f32.png" width="400px">|
<br>
(Dg: Chicken type Dilemma, Dr: Stag-Hunt type Dilemma) <br>

<br>
Network topology can be selected from these three types.<br>
1.　Lattice(2D Grid, default setting)<br>
2.　Random Regular Network (Equally mixed network) <br>
3.　Barabashi-Albert Scale Free Network (Typically observed in SNS) <br>
<br>
