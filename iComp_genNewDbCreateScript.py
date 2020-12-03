import sys

if sys.version_info[0] < 3:
    sys.stdout.write("\n\nRun with python3\n\n")
    sys.exit()
else:
    pass

##Creates .sql file to use to create iComp database
dbName      = input('Enter Database Name:  ')
appServerIp = input('IP/URL of Application Server:  ')
roPwd       = input('password for readonly user:  ')
altPwd      = input('password for alter user:  ')

createDB = "CREATE DATABASE /*!32312 IF NOT EXISTS*/ `" + dbName + "` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;\n"
useDB    = "use `" + dbName + "`;\n"

mainScript = """
DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `name` text CHARACTER SET latin1 NOT NULL,
  `series` text CHARACTER SET latin1 NOT NULL,
  `eventNum` int(11) NOT NULL,
  `live` int(1) NOT NULL,
  `enableFastLapBonus` int(11) NOT NULL,
  `finished` int(11) NOT NULL DEFAULT 0,
  `winner` text CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `participants` (
  `username` text CHARACTER SET latin1 NOT NULL,
  `eventNum` int(11) NOT NULL,
  `vehicle` text CHARACTER SET latin1 NOT NULL,
  `userNum` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `requestedChanges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requestedChanges` (
  `reqNum` int(11) NOT NULL,
  `userNum` int(11) NOT NULL,
  `userName` text CHARACTER SET latin1 NOT NULL,
  `curPoints` int(11) NOT NULL,
  `curInc` int(11) NOT NULL,
  `curPosition` int(11) NOT NULL,
  `newPoints` int(11) NOT NULL,
  `newInc` int(11) NOT NULL,
  `newPosition` int(11) NOT NULL,
  `eventNum` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  PRIMARY KEY (`reqNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule` (
  `eventNum` int(11) NOT NULL,
  `Week` int(11) NOT NULL,
  `track` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `scoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scoring` (
  `eventNum` int(11) NOT NULL,
  `week` int(2) NOT NULL,
  `userNum` int(11) NOT NULL,
  `points` int(3) NOT NULL,
  `inc` int(2) NOT NULL,
  `position` int(2) NOT NULL,
  `changeRequested` int(1) NOT NULL DEFAULT 0,
  `fastLap` text CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userName` text CHARACTER SET latin1 NOT NULL,
  `firstName` text CHARACTER SET latin1 NOT NULL,
  `lastName` text CHARACTER SET latin1 NOT NULL,
  `password` text CHARACTER SET latin1 NOT NULL,
  `admin` int(1) NOT NULL DEFAULT 0,
  `userNum` int(5) NOT NULL,
  `email` text CHARACTER SET latin1 NOT NULL,
  `wins` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`userNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicles` (
  `eventNum` int(11) NOT NULL,
  `vehicle` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `topLap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topLap` (
  `eventNum` int(11) NOT NULL,
  `weekNum` int(11) NOT NULL,
  `userNum` int(11) NOT NULL,
  `laptime` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `iComp_schema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iComp_schema` (
  `version` text CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
LOCK TABLES `iComp_schema` WRITE;
/*!40000 ALTER TABLE `iComp_schema` DISABLE KEYS */;
INSERT INTO `iComp_schema` VALUES ('1.01');
/*!40000 ALTER TABLE `iComp_schema` ENABLE KEYS */;
UNLOCK TABLES;


"""

createLocalRO       = "create user 'iCompRead'@'localhost' identified by '" + roPwd + "';\n" 
createLocalAlt      = "create user 'iCompAlt'@'localhost' identified by '" + altPwd + "';\n" 
permissionsLocalRO  = "grant select on " + dbName + ".* to 'iCompRead'@'localhost';\n" 
permissionsLocalAlt = "grant select, insert, delete, update on " + dbName + ".* to 'iCompAlt'@'localhost';\n" 
createAppRO         = "create user 'iCompRead'@'" + appServerIp + "' identified by '" + roPwd + "';\n" 
createAppAlt        = "create user 'iCompAlt'@'" + appServerIp + "' identified by '" + altPwd + "';\n" 
permissionsAppRO    = "grant select on " + dbName + ".* to 'iCompRead'@'" + appServerIp + "';\n" 
permissionsAppAlt   = "grant select, insert, delete, update on " + dbName + ".* to 'iCompAlt'@'" + appServerIp + "';\n" 

fh = open("./iComp_createDB.sql",'w')

fh.write(createDB)
fh.write(useDB)
fh.write(mainScript)
fh.write(createLocalRO)
fh.write(createLocalAlt)
fh.write(permissionsLocalRO)
fh.write(permissionsLocalAlt)
if appServerIp.lower() != 'localhost' and appServerIp.lower() != '127.0.0.1':
  fh.write(createAppRO)     
  fh.write(createAppAlt)    
  fh.write(permissionsAppRO)
  fh.write(permissionsAppAlt)
else:
  pass

fh.close()


sys.stdout.write('\n\nCreated script at ./iComp_createDB.sql\n')
sys.stdout.write('Run this script on your mysql server to create database for iCompetition\n')
