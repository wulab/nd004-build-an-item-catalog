drop table if exists categories;
create table categories (
  id integer primary key autoincrement,
  name text not null
);

insert into categories (name)
values ('Uncategoried'),
       ('Books'),
       ('Movies'),
       ('Music'),
       ('Games');

drop table if exists items;
create table items (
  id integer primary key autoincrement,
  title text not null,
  note text,
  purchase_price real,
  image_url text,
  category_id integer not null
);

insert into items (title, note, purchase_price, image_url, category_id)
values ( 'Star Wars: The Force Awakens',
         'As a new threat to the galaxy rises, Rey, a desert scavenger, and Finn, an ex-stormtrooper, must join Han Solo and Chewbacca to search for the one hope of restoring peace. Experience the motion picture event of a generation in The Force Awakens.',
         14.99,
         'https://images-na.ssl-images-amazon.com/images/I/91nwbdP8GxL._RI_SX200_.jpg',
         3 ),
       ( 'Star Wars: The Force Awakens Incredible Cross-Sections',
         'See the vehicles of Star Wars: The Force Awakens in unparalleled detail with this newest addition to the Star Wars Incredible Cross Sections series. Twelve breathtaking artworks bring the new craft to life, showing all the weapons, engines, and technology, while engaging text explains each vehicle''s backstory and key features.',
         13.99,
         'https://images-na.ssl-images-amazon.com/images/I/51Y6Pkuv2gL._SX376_BO1,204,203,200_.jpg',
         2 ),
       ( 'Star Wars: The Force Awakens (Original Motion Picture Soundtrack)',
         'John Williams',
         30.12,
         'https://images-na.ssl-images-amazon.com/images/I/51nQZbicKUL.jpg',
         4 ),
       ( 'Star Wars Battlefront II',
         'PlayStation 4',
         42.00,
         'https://images-na.ssl-images-amazon.com/images/I/71an0z4csGL._AC_SX430_.jpg',
         5 );