# SPD
Multi agent simulation code of Prisoner's Dilemma Game on a complex network topology.<br>

<img src="https://user-images.githubusercontent.com/39644776/41784084-9bb5b1b4-7679-11e8-87be-2401128dd9a6.png" width="400px" title="Image of the game on lattice">
When running the simulation,just type <br>
$ python SPD.py <br>
After that, many output files will be generated. You can visualize the result with heatmap.py.<br>
$ python heatmap.py <br>
<br>
Depending on the topology and strategy update rule, you can see various Dg-Dr diagram.<br>
<br>

|Imitation max strategy update on lattice|Pairwise-Fermi strategy update on BA-Scale Free network|
|:---:|:---:|
|<img src="https://user-images.githubusercontent.com/39644776/41786084-79b1138c-767f-11e8-9316-b81229a3dcdf.png" width="400px">|<img src="https://user-images.githubusercontent.com/39644776/41786092-7e3ee1d6-767f-11e8-95c3-6523d7392f32.png" width="400px">|
<br>

<br>
Network topology can be selected from these three types.<br>
1.　Lattice(2D Grid, default setting)<br>
2.　Random Regular Network<br>
3.　Barabashi-Albert Scale Free Network<br>
<br>
