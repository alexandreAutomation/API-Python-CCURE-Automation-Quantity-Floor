WITH CTE1 AS (SELECT
					ObjectIdentity1,
					Andar_,
					Empresa_,
					Personnel.GUID,
					PersonnelUDF.ObjectID,
					ObjectName1,
					MessageType,
					ObjectName3,
					ObjectName2,
					CONVERT(DATETIME,SWITCHOFFSET(CONVERT(DATETIMEOFFSET, MessageUTC),'-03:00')) AS Datahora,
					ROW_NUMBER() OVER(PARTITION BY ObjectIdentity1 ORDER BY
					CONVERT(DATETIME,SWITCHOFFSET(CONVERT(DATETIMEOFFSET, MessageUTC),'-03:00')) DESC) AS ordem

					FROM
						ACVSUJournal_00010006.DBO.ACVSUJournalLog,
						ACVSCore.Access.PersonnelUDF,
						ACVSCore.Access.Personnel

				WHERE MessageType = 'CardAdmitted' and
					  MessageUTC BETWEEN '2021-1-11 00:00:00' and '2021-30-11 23:59:59'and
					  --cast (MessageUTC as date) = cast(getdate() as date) and
					  Personnel.GUID = ObjectIdentity1 and
					  Personnel.ObjectID = PersonnelUDF.ObjectID
)SELECT
	Andar_ Andar,
	CASE WHEN ObjectName3 like '%Torre 01%'THEN 'T1' WHEN ObjectName3 like '%Torre 02%'THEN 'T2' ELSE 'AC' end AS 'Local',
    count(Andar_) Quantidade, Empresa_

       FROM (
			 SELECT
			      ObjectIdentity1,
				  Datahora,
				  Andar_,
				  Empresa_,
				  ObjectName1,
				  ObjectName2,
				  ObjectName3,
				  ordem
from CTE1) as res

where ordem = 1 and
(ObjectName3 like '%Dentro%' or (ObjectName3 IS NULL and ObjectName2 like '%PORTA%'))

group by Andar_, ObjectName3, Empresa_

order by Local , Andar_ desc