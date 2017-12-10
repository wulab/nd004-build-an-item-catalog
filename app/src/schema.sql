drop table if exists items;
create table items (
  id integer primary key autoincrement,
  title text not null,
  description text not null
);
