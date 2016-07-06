/**
* @Author: Samaksh Jain <ybl>
* @Date:   Wednesday, July 6th 2016, 11:40:20 am(IST)
* @Email:  samakshjain@live.com
* @Last modified by:   ybl
* @Last modified time: Wednesday, July 6th 2016, 8:43:31 pm(IST)
* @License: MIT
*/


drop table if exists blag;
create table blag (
	  id integer primary key autoincrement,
	  heading text not null,
	  content text not null
);
