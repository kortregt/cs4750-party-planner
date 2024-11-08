CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<complex password>';
GO

CREATE CERTIFICATE CustomerContactCert
WITH SUBJECT = 'Customer Contact Information';
GO

ALTER TABLE Customer
ADD phone_number_encrypted VARBINARY(256);
GO

UPDATE Customer
SET phone_number_encrypted = EncryptByKey(Key_GUID('CustomerContactCert'), phone_number);
GO
