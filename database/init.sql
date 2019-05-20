create table users
(
	userID int auto_increment,
	username text not null,
	password varchar(255) not null,
	firstName tinytext not null,
	lastName tinytext not null,
	email text not null,
	constraint users_pk
		primary key (userID)
);

create unique index users_username_uindex
	on users (username);
