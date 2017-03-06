drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null,
  email text,
  telephone integer,
  enabled integer not null,
  create_at text not null,
  last_active_at text,
  extra text
);

insert into users (id, name, enabled, create_at) values (1, 'admin', 1, '2017-03-06 10:16:00');

drop table if exists roles;
create table roles (
  id integer primary key autoincrement,
  name text not null,
  enabled integer not null,
  create_at text not null,
  last_active_at text,
  extra text
);

insert into roles (id, name, enabled, create_at) values (1, 'administrator', 1, '2017-03-06 10:16:00');

drop table if exists user_group;
create table users (
  id integer primary key autoincrement,
  name text not null,
  description text,
  enabled integer not null,
  create_at text not null,
  last_active_at text,
  extra text
);
insert into user_group (id, name, enabled, create_at) values (1, 'administrators', 1, '2017-03-06 10:16:00');

drop table if exists rights;
create table rights (
  id integer primary key autoincrement,
  name text not null,
  'value' integer not null,
  description text,
  enabled integer not null,
  create_at text not null,
  last_active_at text,
  extra text
);
insert into rights (id, name, 'value', enabled, create_at) values (1, 'retrieve', 1, 1, '2017-03-06 10:16:00');
insert into rights (id, name, 'value', enabled, create_at) values (1, 'create', 2, 1, '2017-03-06 10:16:00');
insert into rights (id, name, 'value', enabled, create_at) values (1, 'update', 3, 1, '2017-03-06 10:16:00');
insert into rights (id, name, 'value', enabled, create_at) values (1, 'delete', 4, 1, '2017-03-06 10:16:00');

drop table if exists resources;
create table resources (
  id integer primary key autoincrement,
  name text not null,
  description text,
  enabled integer not null,
  create_at text not null,
  last_active_at text,
  extra text
);
insert into resources (id, name, enabled, create_at) values (1, 'admin', 1, '2017-03-06 10:16:00');

drop table if exists id_maps;
create table id_maps (
  id integer primary key autoincrement,
  user_id integer not null,
  role_id integer not null,
  right_id integer not null,
  resource_id integer not null,
  create_at text not null,
  last_update_at text,
  extra text
);
insert into id_maps (id, user_id, role_id, right_id, resource_id, create_at) values (1, 1, 1, 1, 1, '2017-03-06 10:16:00');

drop table if exists password;
create table password (
  id integer primary key autoincrement,
  user_id integer not null,
  password text not null,
  create_at text not null,
  expires_at text,
  extra text
);
insert into password (id, user_id, password, create_at) values (1, 1, 'abc123', '2017-03-06 10:16:00');