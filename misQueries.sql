delete from dbo.Processes where processnumber = 2510 or processnumber = 3408;

delete from dbo.Requests where processId is null;

select * from dbo.Processes where processnumber = 2510 or processnumber = 3408;

select * from dbo.Requests;

INSERT INTO requests 
(createdat, updatedat, servicetype, processId) VALUES
('2018-06-15','5/21/2019','coe team discovery', (SELECT dbo.Processes.processId FROM dbo.Processes WHERE dbo.Processes.processNumber='2510'));