select * from dbo.Processes;
select * from dbo.Requests;
select * from dbo.Users;
select * from dbo.Statuses;

delete from dbo.Processes;
delete from dbo.Requests;
delete from dbo.Users;
delete from dbo.Statuses;


insert into dbo.Statuses (description, createdAt, updatedAt) values 
('NEW','2019-07-25','2019-07-25'),
('IN PROGRESS','2019-07-25','2019-07-25'),
('COMPLETED','2019-07-25','2019-07-25'),
('CANCELLED','2019-07-25','2019-07-25'),
('ON HOLD','2019-07-25','2019-07-25');





-- update values in Requests
update dbo.Requests set dbo.Requests.processId=(select dbo.Processes.processId from dbo.Processes where dbo.Processes.processId=dbo.Requests.id) ;
update dbo.Requests set dbo.Requests.requestUser=(
	select dbo.Users.id from dbo.Users where dbo.Users.updatedAt = dbo.Requests.updatedAt
);
update dbo.Requests set dbo.Requests.overallStatusCode=342;

select * from dbo.Requests;

-- =CONCAT("2019-07-25T",TEXT(RANDBETWEEN(0,23),"00"),":",TEXT(RANDBETWEEN(0,59),"00"),":00.00Z")