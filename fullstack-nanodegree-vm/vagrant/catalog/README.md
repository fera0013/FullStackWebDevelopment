Catalog app
========================

The catalog-app implements a complete CRUD workflow using Flask. 
Main focus was the development of the backend, the app therefore
has only a very basic frontend.

To run the app, follow these steps:

1. Install Vagrant and VirtualBox
2. Open a git bash in the /vagrant subfolder
3. enter "vagrant up" to start the vagrant vm
4. enter "vagrant ssh" to establish an ssh connection 
5. cd into /vagrant/catalog
6. enter "python runserver.py" to start the webserver for the app
7. use the address "http://localhost:53224/" to access the app through a browser
8. enter "ctrl c" in the git bash to stopp the webserver
9. enter "exit" to exit linux
10. enter "vagrant halt" to shut down the vm.

To change the port of the webserver, edit runserver.py. 