# Stochastic Simulation
These are my course projects of Stochastic Simulation in Peking University. Please refer to Professor Li's [website](http://dsec.pku.edu.cn/~tieli/) for more project details. If you have any problems, please contact me with **yangwhsms@gmail.com**
## Project 1
Just run the following command:

`$ python main.py`

The default number of workers is 32. Please change the number of workers according to your machine's threading number before you run this file.

## Project 6
There are two simulation methods 'Euler-Maruyama', 'Milstein scheme'.

Single Monte Carlo Method has been implemented. Please run the following command:

`$ cd project6`

`$ python main.py -- --algorithm Euler-Maruyama --method mc`

The default number of workers is `16` and divide the time into `2^8` and simulate `100000` times. The default would cost about `6s`
