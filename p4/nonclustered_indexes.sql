CREATE NONCLUSTERED INDEX IX_Reservation_Date
ON Reservation(date)
INCLUDE (venue_id, start_time, end_time);

CREATE NONCLUSTERED INDEX IX_Party_Type
ON Party(type)
INCLUDE (booking_id, description);

CREATE NONCLUSTERED INDEX IX_Caterer_Location
ON Caterer(location)
INCLUDE (business_name, cuisine, phone_number);
GO