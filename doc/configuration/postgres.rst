.. sectnum::

Postgres
========

General considerations
-----------------------------------

In order to perform actions like backup/restore, we must at first provide access to the service. This means we have to:

#. expose database port (5432 by default)
#. create or use an existing account
#. list of IP addresses from which given account will be able to connect
#. list of databases to which this account have access

To see detailed guide on this topic, please have a look at the `official <https://www.postgresql.org/docs/current/auth-pg-hba-conf.html>`_
page. Please try **not** use ``md5``, but rather ``scram-sha-256`` for password verification because it has major
weaknesses:

* password guessing
* replay attack
* stolen hash

.. warning::

   Each user password hash is saved in the table ``pg_authid``. It includes the hashing algorithm that is used to
   transform the password to its hash.

   When setting the password_encryption in postgresql.conf, you are setting the default encryption, i.e. the one used
   when creating a user or when (re)setting your password. The table pg_authid is **not** updated.

   When changing pg_hba.conf, you are saying to accept only passwords hashed using the given method. The table
   ``pg_authid`` is **not** updated.

   So, if you wish to update system *already* using ``md5``, the solution is to

   #. start with the existing users
   #. update postrgres.conf to use scram and reload the configuration
   #. reset the user password: it will now be saved as scram in pg_authid
   #. you can still use md5 in pg_hba.conf
   #. when happy with the move from md5 to scram, update pg_hba.conf to specify scram instead of md5

You can also consider using certificates in case access to the database has to be done from a remote host - which
sometimes can not be avoided - say when service consuming database is located on another host (Keycloak for example).

Obtaining server information
-----------------------------------

To get location of the postgres and hba configuration files and also server version, login to machine where Postgres is
running (using superuser account):

.. code-block:: bash

   sudo su - postgres
   psql -qAtX -c 'SHOW config_file;'
   psql -qAtX -c 'SHOW hba_file;'
   psql -qAtX -c 'SHOW server_version;' | awk '{print $1}'

Backup/Restore procedure
-----------------------------------

We must have access to `pg_dump <https://www.postgresql.org/docs/current/app-pgdump.html>`_ and
`pg_restore <https://www.postgresql.org/docs/current/app-pgrestore.html>`_ - either as locally installed package or by
using i.e. `postgres <https://hub.docker.com/_/postgres>`_ Docker image. Both of these approaches are valid, but more
complex.

What we are going to use is to access the remote host (where PostgreSql is running) as user with sufficient
privileges to execute commands as built-in or dedicated user. This can be achieved in multiple ways:

* `fabric <https://www.fabfile.org/>`_ - library designed to execute shell commands remotely over SSH, yielding useful
  Python objects in return
* `ansible <https://docs.ansible.com/ansible/latest/index.html>`_ - an IT automation tool. It can configure systems,
  deploy software, and orchestrate more advanced IT task
* `salt <https://gitlab.com/saltstack/open/salt>`_ - remote execution framework for configuration management,
  automation, provisioning, and orchestration.

Built-in user
+++++++++++++++++++++++++++++++++++++++++++++++++++

Assuming ``postgres`` is the database superuser, login to machine where Postgres is running (using superuser account):

.. code-block:: bash

   sudo su - postgres
   pg_dump -d keycloak -h localhost -p 5432 -U postgres --format=custom --if-exists --clean --no-owner --no-acl -f /tmp/keycloak.dump

Dedicated user
+++++++++++++++++++++++++++++++++++++++++++++++++++

Login to machine where Postgres is running (using superuser account). We are going to:
* allow Postgres to listen on all available interfaces
* create a new role - *backup* (do not forget to use appropriate username and password!)
* allow this new role to access from each host to all databases (this is why it is important **not** to use md5, as we
mentioned already)
* restart service

.. code-block:: bash

   sudo su - postgres
   CONFIG_FILE=$(psql -qAtX -c 'SHOW config_file;')
   sed -i -e "/listen_addresses/c\listen_addresses = '*'" ${CONFIG_FILE}
   psql -c "CREATE ROLE backup WITH CREATEDB LOGIN ENCRYPTED PASSWORD 'univention'";
   HBA_FILE=$(psql -qAtX -c 'SHOW hba_file;')
   echo -e "host\tall\t\tbackup\t\tall\t\t\tmd5" >> ${HBA_FILE}
   exit
   sudo service postgresql restart


To perform backup, we use (note that we dont have to switch account, can directly be run under say *root* account):

.. code-block:: bash

   PGPASSWORD="univention" pg_dump -d keycloak -h localhost -p 5432 -U backup --format=custom --if-exists --clean --no-owner --no-acl -f /tmp/keycloak.dump
