drop table if exists wishlist;
create table wishlist (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
