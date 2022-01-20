show databases;

use onoffmix;

show tables;

create table User(
		user_no		  int 		    not null 	auto_increment 	primary key,
		user_name 	  varchar(255) 	not null,
		user_pw 	  varchar(255) 	not null,
		user_mail     varchar(255)  not null,
		user_created  datetime      default now(),
		user_updated  datetime      default now()
);

create table Meet(
		meet_no		  int 		    not null 	auto_increment 	primary key,
		meet_title 	  varchar(255) 	not null,
		meet_content  varchar(255) 	not null,
		meet_view     int           not null,
		meet_created  datetime      default now(),
		meet_updated  datetime      default now(),
        
		user_no	 	  int	      	not null,
        
		foreign key (user_no)
		references User(user_no) on update cascade
);

create table Form(
		form_no 			int 		    not null auto_increment primary key,
		form_title     		varchar(255) 	not null,
		form_total 	    	int(4) 		    not null,
		form_admission 		char(1) 		not null,
		form_meet_start		datetime      	not null,
		form_meet_end  		datetime      	not null,
		form_apply_start 	datetime    	not null,
		form_apply_end 	    datetime    	not null,
		form_created 		datetime 		default now(),
		form_updated 		datetime 		default now(),
			
		meet_no 	    	int 		    not null,

		foreign key (meet_no)
		references Meet(meet_no) on update cascade
);

create table FormUser(
		formuser_no 	int 		   	not null	auto_increment 	primary key,
		meet_no 		int 			not null,
		form_no 		int 		  	not null,
		user_no 		int 		  	not null,
		user_static		char(1)			not null,
		formuser_state 	char(1) 		not null,
		form_reason     varchar(255)  	not null,
		
		foreign key (meet_no)
		references Meet(meet_no) on update cascade,
		foreign key (form_no)
		references Form(form_no) on update cascade,
		foreign key (user_no)
		references User(user_no) on update cascade
);

select * from User;
select * from Meet;
select * from Form;
select * from FormUser;

alter table FormUser modify column form_reason varchar(255);
desc FormUser;

select * from FormUser where form_no = 4;

desc Meet;

-- insert into User(user_name, user_pw, user_mail) values(-- );

insert into Meet(meet_title, meet_content, meet_view, user_no) values('안녕하세요', '안녕하세요 모임에 오신 여러분 환영합니다', 1, 1);
insert into Meet(meet_title, meet_content, meet_view, user_no) values('반갑습니다', '반갑습니다 모임에 오신 여러분 환영합니다', 1, 1);

insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no) 
values('안녕하세요 그룹1', 100, 'G', "2022-02-02 15:00:00", "2022-02-02 18:00:00", "2022-01-20 00:00:00", "2022-01-30 00:00:00", 1);
insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no)
values('안녕하세요 그룹2', 200, 'S', "2022-02-02 18:00:00", "2022-02-02 21:00:00", "2022-01-21 00:00:00", "2022-01-31 00:00:00", 1);
insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no) 
values('반갑습니다 그룹1', 100, 'G', "2022-03-02 15:00:00", "2022-03-05 18:00:00", "2022-02-20 00:00:00", "2022-02-28 00:00:00", 2);
insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no)
values('반갑습니다 그룹2', 200, 'S', "2022-03-02 18:00:00", "2022-03-05 21:00:00", "2022-02-21 00:00:00", "2022-02-28 00:00:00", 2);

-- MeetUser -- 
insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason) values (1, 1, 1, 'M', 'N', '안녕하세요');
insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason) values (1, 1, 2, 'P','N', '안녕하세요');
insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason) values (2, 3, 1, 'M','N', '반갑습니다');
insert into FormUser(meet_no, form_no, user_no, user_static, formuser_state, form_reason) values (2, 4, 3, 'P','N', '반갑습니다');

select user_no from FormUser
            where meet_no = 1 and user_no = 4;
            
select count(user_no) from User
            where user_no = 1;

-- 행사가 종료되지 않은 모임 리스트 (신청자 수 -> 조회수 -> 최신순)
select m.meet_no, m.meet_title, m.meet_created, m.meet_view, f.form_no, form_title, u.member from Form as f 
inner join (select form_no, count(user_no) as member from FormUser group by form_no) as u
on f.form_no = u.form_no
join Meet as m 
on f.meet_no = m.meet_no
where date(f.form_meet_end) > date(now())
group by f.form_no, u.member
order by u.member desc, m.meet_view desc, m.meet_created desc;
      
-- 모임 상세
select * from Meet where meet_no = 1;

-- 해당 모임에 인원수 

select f.* from Meet as m right join Form as f 
                on m.meet_no = f.meet_no 
                where m.meet_no = 1;

select meet_no, meet_title, meet_created, meet_view, 
	(select count(user_no) as c from FormUser 
	where meet_no = 1
    group by meet_no) as meet_member 
from Meet
where meet_no = 1;									

-- 조회수
update Meet set meet_view = (select meet_view) + 1 where meet_no = 1;

delete from Meet where meet_no = 27;

select form_no from Form 
where form_no = 1 and form_total >= ( select count(user_no) as c from FormUser
                                            where meet_no = 1
                                            group by meet_no);
                           
select * from Meet;
select * from Form;
select * from FormUser;
delete from Meet where meet_no = 34; 
delete from Form where form_no = 15;                      
                                            
-- createMeet
select meet_title from Meet where meet_title = "{meet_title}";
                
insert into Meet(meet_title, meet_content, meet_view, user_no) values ("{meet_title}", "{meet_content}", 0, user_no);

select meet_no from Meet where user_no = user_no and meet_title = "{meet_title}";

-- insert into Form(form_title, form_total, form_admission, form_meet_start, form_meet_end, form_apply_start, form_apply_end, meet_no)
-- values("{i["form_title"]}", {i["form_total"]}, "{i["form_admission"]}", "{i["form_meet_start"]}", "{i["form_meet_end"]}", "{i["form_apply_start"]}", "{i["form_apply_end"]}", {meet});

select form_no from Form where form_title = "어서오세요 그룹1";


-- 참가자 리스트 보여주기

select fu.meet_no, fu.form_no, fu.formuser_state, fu.form_reason, u.user_no, u.user_name, u.user_mail from FormUser as fu  join User as u
on fu.user_no = u.user_no
where user_static = 'P' and form_no = 3; 

select * from FormUser where user_no = 1 and user_static="M" ;

select meet_no from FormUser where user_no = 1 and user_static="M" group by meet_no;

select form_no from FormUser where meet_no = 35 and user_static="M" group by form_no;

select fu.meet_no, fu.form_no, fu.formuser_state, fu.form_reason, u.user_name from FormUser as fu join User as u on fu.user_no = u.user_no where form_no = 16 and user_static= "P";

select * from FormUser as fu join Form as f on fu.form_no = f.form_no where fu.form_no = 16;