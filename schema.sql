create table users
(
    user_id                serial      not null
        constraint users_pkey
            primary key,
    first_name             varchar(50) not null,
    last_name              varchar(50) not null,
    email                  varchar(50) not null
        constraint users_email_key
            unique,
    pwd                    varchar     not null,
    last_message_read_time timestamp,
    isadmin                boolean,
    reward                 integer default 0
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
    active         boolean default true,
    word_vector    double precision[]
);

alter table items
    owner to myadmin;

create unique index items_item_id_uindex
    on items (item_id);

create table messages
(
    id           serial not null
        constraint messages_pk
            primary key,
    sender_id    integer
        constraint messages_users_user_id_fkey
            references users,
    recipient_id integer
        constraint messages_users_user_id_fk
            references users,
    body         varchar(500),
    timestamp    timestamp,
    item_id      integer
        constraint messages_items_item_id_fk
            references items
);

alter table messages
    owner to myadmin;

create table notification
(
    id           serial not null
        constraint notification_pk
            primary key,
    name         varchar(128),
    user_id      integer
        constraint notification_users_user_id_fk
            references users,
    timestamp    timestamp,
    payload_json varchar(500)
);

alter table notification
    owner to myadmin;

