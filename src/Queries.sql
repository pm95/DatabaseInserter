select * from dbo.Processes where processnumber = 2510 or processnumber = 3408;
select * from dbo.Requests;
select * from dbo.Users where userId is null;
select * from dbo.Statuses where updatedAt = '2019-05-21';

delete from dbo.Processes where processnumber = 2510 or processnumber = 3408;
delete from dbo.Requests where requestUser is null;
delete from dbo.Users where userId is null;
delete from dbo.Statuses where updatedAt = '2019-05-21';

update dbo.Requests set dbo.Requests.processId=(select dbo.Processes.processId from dbo.Processes where dbo.Processes.createdAt='2018-06-15') where dbo.Requests.createdAt = '2018-06-15';
update dbo.Requests set dbo.Requests.requestUser=(select dbo.Users.id from dbo.Users where dbo.Users.createdAt='2018-06-15') where dbo.Requests.createdAt = '2018-06-15';
update dbo.Requests set dbo.Requests.overallStatusCode=(select dbo.Statuses.statusCode from dbo.Statuses where dbo.Statuses.createdAt='2018-06-15') where dbo.Requests.createdAt = '2018-06-15';



INSERT INTO requests 
(createdat, updatedat, servicetype, processId) VALUES
('2018-06-15','5/21/2019','coe team discovery', 
(SELECT dbo.Processes.processId FROM dbo.Processes WHERE dbo.Processes.processNumber='2510')
);