drop table if exists users;
    create table users (
    id int(10) primary key NOT NULL ,
    username text not null,
    password text not null
);
create table awsconfig (
    id int(10) primary key NOT NULL ,
    AWS_ACCESS_KEY_ID text not null,
    AWS_SECRET_ACCESS_KEY text not null,
    AWS_REGION_NAME text not null,
    AWS_Account_ID text not null

);

drop table if exists registry;
    create table registry (
    id int(10) primary key NOT NULL ,
    registry text not null,
    registry_username text not null,
    registry_password text not null
);

drop table if exists images;
    create table images (
    id int(10) primary key NOT NULL ,
    image_name text not null,
    repo_name text not null,
    registry text not null
);

drop table if exists swarm;
CREATE TABLE swarm (
    swarmid varchar(255) ,
    swarmname varchar(255) ,
    createdate date,
    workerdisksize int,
    enablecloudwatchlogs varchar(3) ,
    managerdisksize int,
    enablesystemprune varchar(3),
    clustersize int,
    keyname varchar(15) ,
    managerdisktype varchar(8) ,
    managersize int,
    workerdisktype varchar(8) ,
    instancetype varchar(8) ,
    managerinstancetype varchar(8) ,
    stackstaus varchar(8),
    dnsname varchar(255)
);


insert into swarm(stackid,swarmname,createdate,dnsname) values('arn:aws:cloudformation:us-west-2:493665568723:stack/docker5/c8d44a20-eba0-11e7-9a48-503ac9ec2435','docker5','Thu, 14 Dec 2017 06:00:21 GMT','docker5-ExternalLo-172EP4GKXS94J-1421184407.us-west-2.elb.amazonaws.com');
insert into swarm(stackid,swarmname,createdate, dnsname) values('arn:aws:cloudformation:us-west-2:493665568723:stack/docker6/c8d44a20-eba0-11e7-9a48-503ac9ec2435','docker6','Thu, 14 Dec 2017 06:00:21 GMT','docker6-ExternalLo-172EP4GKXS94J-1421184407.us-west-2.elb.amazonaws.com');

DROP TABLE IF EXISTS managerdetails;

CREATE TABLE managerdetails(
    swarmid varchar(255) ,
    swarmname varchar(255),
    managerhostname varchar(255) ,
    managerip varchar(255) ,
    engineversion varchar(255) ,
    availablity varchar(255) ,
    state varchar(20)
);

DROP TABLE IF EXISTS workerdetails;
CREATE TABLE workerdetails(
    swarmid varchar(255) ,
    swarmname varchar(255) ,
    workerhostname varchar(255) ,
    workerip varchar(255) ,
    state varchar(20)
);

drop table if exists stack;
CREATE TABLE stack (
    `StackId` VARCHAR(96) CHARACTER SET utf8,
    `date` VARCHAR(29) CHARACTER SET utf8,
    `WorkerDiskSize` INT,
    `EnableCloudWatchLogs` VARCHAR(3) CHARACTER SET utf8,
    `ManagerDiskSize` INT,
    `EnableSystemPrune` VARCHAR(2) CHARACTER SET utf8,
    `ClusterSize` INT,
    `KeyName` VARCHAR(15) CHARACTER SET utf8,
    `ManagerDiskType` VARCHAR(8) CHARACTER SET utf8,
    `ManagerSize` INT,
    `WorkerDiskType` VARCHAR(8) CHARACTER SET utf8,
    `InstanceType` VARCHAR(8) CHARACTER SET utf8,
    `ManagerInstanceType` VARCHAR(8) CHARACTER SET utf8,
    `StackStaus` VARCHAR(8) CHARACTER SET utf8
);

drop table if exists service;
create table service(
    ServiceId int(10) primary key NOT NULL ,
    SwarmName VARCHAR(20) ,
    SwarmURL VARCHAR(20) ,
    ServiceName VARCHAR(20) ,
    ImageName VARCHAR(20) ,
    HostPort int,
    ContainerPort int,
    DockerRegistry VARCHAR(20),
    Replicas int
);

insert into users (id,username,password) VALUES(1,'$2b$12$lMLmKaGGPeoCP6M41uw2ae4XbulberuBi5pmG7vJs.TlETziXY2xK','$2b$12$1oSp3thFXbN7TDzGOMib1.Yq.vvrgtDLtWdZTypYZPU/ZZnZNSoaO');
insert into awsconfig (id,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION_NAME) VALUES(1,'AKIAJOICH7L4GJP3CBNQ','ZroQDUEvrIrjTICzjwDRt1boYDj1a3W1uQXaD8/8','us-west-2','493665568723');
INSERT INTO swarm VALUES ('arn:aws:cloudformation:us-west-2:493665568723:stack/docker1/11c53d10-e094-11e7-99fe-50d5ca789ee6','Thu, 14 Dec 2017 06:00:21 GMT',20,'yes',20,'no',2,'sigmaex2KeyPair','standard',1,'standard','t2.micro','t2.micro');