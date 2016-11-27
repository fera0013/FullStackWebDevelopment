Swiss pairing tournament
========================

The code in the /vagrant/tournament subfolder implements a postgreSQL-based swiss pairing system as specified at

https://classroom.udacity.com/nanodegrees/nd004/parts/0041345405/modules/353202897075461/lessons/3532028970239847/concepts/35196892840923# .

To run the code, follow these steps:

1. Install Vagrant and VirtualBox
2. Open a git bash in the /vagrant folder
3. enter "vagrant up" to start the vagrant vm
4. enter "vagrant ssh" to establish an ssh connection 
5. cd into /vagrant/tournament
6. Create the project's database through the following sequence of commands:
 - vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ \psql
 - vagrant=> \i tournament.sql
 - tournament=> \q
7. run the tournament unit tests using the command $ python tournament_test.py
