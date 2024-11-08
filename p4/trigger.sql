IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'tr_Reservation_CheckCapacity')
    DROP TRIGGER tr_Reservation_CheckCapacity
GO

CREATE TRIGGER tr_Reservation_CheckCapacity
ON Reservation
INSTEAD OF INSERT, UPDATE
AS
BEGIN
    INSERT INTO Reservation (
        booking_id, date, number_of_guests, start_time, end_time,
        venue_id, organizer_id, caterer_id, customer_id
    )
    SELECT 
        i.booking_id, i.date, i.number_of_guests, i.start_time, i.end_time,
        i.venue_id, i.organizer_id, i.caterer_id, i.customer_id
    FROM inserted i
    JOIN Venue v ON i.venue_id = v.venue_id
    WHERE i.number_of_guests <= v.max_capacity;
END;
GO