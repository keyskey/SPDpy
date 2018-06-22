# SPD
Multi agent simulation code of Prisoner's Dilemma Game on a complex network topology.<br>

<img src="https://user-images.githubusercontent.com/39644776/41784084-9bb5b1b4-7679-11e8-87be-2401128dd9a6.png" width="400px" title="Image of the game on lattice">
When running the simulation,just type <br>

$ python SPD.py <br>
After that, many output files will be generated. You can visualize the result with heatmap.py.<br>

$ python heatmap.py <br>
<br>

Depending on the topology and strategy update rule, you can see various Dg-Dr diagram.<br>
|Imitation max strategy update on lattice|Pairwise-Fermi strategy update on BA-Scale Free network|
|:---|:---|
![figure_1](https://user-images.githubusercontent.com/39644776/41786084-79b1138c-767f-11e8-9316-b81229a3dcdf.png "Imitation max strategy update on lattice")
![figure_1](https://user-images.githubusercontent.com/39644776/41786092-7e3ee1d6-767f-11e8-95c3-6523d7392f32.png "Pairwise-Fermi strategy update on BA-Scale Free network")


<br>
Network topology can be selected from these three types.
* Lattice(2D Grid, default setting)
* Random Regular Network
* Barabashi-Albert Scale Free Network
<br>
<br>
