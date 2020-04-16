create table users
(
    user_id    serial      not null
        constraint users_pkey
            primary key,
    first_name varchar(50) not null,
    last_name  varchar(50) not null,
    email      varchar(50) not null
        constraint users_email_key
            unique,
    pwd        varchar     not null
);

alter table users
    owner to myadmin;

create table items
(
    item_id        serial not null
        constraint items_pk
            primary key,
    user_id        integer
        constraint items_users_user_id_fk
            references users,
    type           varchar(100),
    location       varchar(100),
    timestamp      timestamp,
    image_path     varchar(300),
    caption        varchar(500),
    feature_vector double precision[],
    active         boolean default true
);

alter table items
    owner to myadmin;

create unique index items_item_id_uindex
    on items (item_id);

