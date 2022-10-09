Overview
========

In order to perform actions like backup/restore, we must at first provide access to the service. This means we have to:

#. expose database port (5432 by default)
#. create or use an existing account
#. list of IP addresses from which given account will be able to connect
#. list of databases to which this account have access

To see detailed guide on this topic, please have a look at the `official <https://www.postgresql.org/docs/current/auth-pg-hba-conf.html>`_
page. Please do **not** use ``md5``, but rather ``scram-sha-256`` for password verification. Also consider using
certificates in case access to the database has to be done from a remote host.
