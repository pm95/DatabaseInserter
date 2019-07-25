select * from dbo.Processes;
select * from dbo.Requests;
select * from dbo.Users;
select * from dbo.Statuses;

delete from dbo.Processes;
delete from dbo.Requests;
delete from dbo.Users;
delete from dbo.Statuses;


-- update values in Requests
update dbo.Requests set dbo.Requests.processId=(select dbo.Processes.processId from dbo.Processes where dbo.Processes.createdAt=dbo.Requests.createdAt and dbo.Processes.updatedAt=dbo.Requests.updatedAt) ;
update dbo.Requests set dbo.Requests.requestUser=(select dbo.Users.id from dbo.Users where dbo.Users.createdAt=dbo.Requests.createdAt and dbo.Users.updatedAt=dbo.Requests.updatedAt);
update dbo.Requests set dbo.Requests.overallStatusCode=(select dbo.Statuses.statusCode from dbo.Statuses where dbo.Statuses.createdAt=dbo.Requests.createdAt and dbo.Statuses.updatedAt=dbo.Requests.updatedAt);

select * from dbo.Requests;

-- =CONCAT("2019-07-25T",TEXT(RANDBETWEEN(0,23),"00"),":",TEXT(RANDBETWEEN(0,59),"00"),":00.00Z")