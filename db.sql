drop table if exists blag;
create table blag (
	  id SERIAL,
	  heading text not null,
	  content text not null
);
