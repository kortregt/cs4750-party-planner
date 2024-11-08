-- Function 1: List caterers in the same city as a given venue and has matching kitchen requirements--
CREATE FUNCTION dbo.ListCaterersNearThisVenue (
    @VenueID INT
)
RETURNS TABLE
AS
RETURN (
    SELECT C.caterer_id, C.business_name, C.cuisine, C.phone_number, C.price_per_order FROM Caterer C
        --same as saying SameCity & (VenueHasAKitchen || (VenueNotHaveKitchen AND CatererNotRequireKitchen))
        WHERE C.[location] = (SELECT V.[location] FROM Venue V WHERE venue_id = @VenueID)
        AND ( EXISTS (SELECT 1 FROM Venue V1 INNER JOIN Venue_amenities A ON V1.venue_id = A.venue_id WHERE V1.venue_id = @VenueID AND A.amenity = 'Kitchen') OR 
        ( NOT EXISTS (SELECT 1 FROM Venue V2 INNER JOIN Venue_amenities A2 ON V2.venue_id = A2.venue_id WHERE V2.venue_id = @VenueID AND A2.amenity = 'Kitchen') AND C.needs_kitchen = 0) )
        )
GO

--Function 2: Returns overlapping reservation(s) given a venue id, date, a start time, and an end time --
CREATE FUNCTION dbo.ListOverlappingReservations(
    @VenueID int,
    @newreservationdate DATE,
    @newreservationstarttime TIME,
    @newreservationendtime TIME
)
RETURNS TABLE
AS
RETURN (
    SELECT 'conflict' AS Conflict, R.start_time, R.end_time FROM Reservation R 
    --if for a given date, the new reservation begins before another one at the same location ends, this means there is a conflict.
    WHERE R.venue_id = @VenueID AND R.[date] = @newreservationdate AND @newreservationstarttime < R.end_time
)
GO

-- Function 3: to check if time is within venue operating hours --
CREATE FUNCTION dbo.IsWithinVenueHours(
    @VenueID INT,
    @StartTime TIME,
    @EndTime TIME
)
RETURNS BIT
AS
BEGIN
    DECLARE @OpenTime TIME
    DECLARE @CloseTime TIME
    DECLARE @IsValid BIT = 0

    SELECT @OpenTime = open_time, @CloseTime = close_time
    FROM Venue
    WHERE venue_id = @VenueID

    IF @StartTime >= @OpenTime AND @EndTime <= @CloseTime
        SET @IsValid = 1

    RETURN @IsValid
END;
GO