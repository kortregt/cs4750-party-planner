IF EXISTS (SELECT * FROM sys.views WHERE name = 'EventDetailsView')
    DROP VIEW EventDetailsView
GO

CREATE VIEW EventDetailsView AS
SELECT 
    r.booking_id,
    r.date,
    v.name AS venue_name,
    p.type AS party_type,
    r.number_of_guests,
    o.name AS organizer_name,
    c.business_name AS caterer_name,
    pgh.name AS guest_of_honor,
    COUNT(DISTINCT rp.performer_id) AS number_of_performers,
    COUNT(DISTINCT rs.staff_id) AS number_of_staff
FROM Reservation r
JOIN Venue v ON r.venue_id = v.venue_id
JOIN Party p ON r.booking_id = p.booking_id
JOIN Organizer o ON r.organizer_id = o.organizer_id
LEFT JOIN Caterer c ON r.caterer_id = c.caterer_id
LEFT JOIN Party_GuestOfHonor pgh ON p.booking_id = pgh.booking_id AND p.party_id = pgh.party_id
LEFT JOIN Reservation_Performers rp ON r.booking_id = rp.booking_id
LEFT JOIN Reservation_Staff rs ON r.booking_id = rs.booking_id
GROUP BY r.booking_id, r.date, v.name, p.type, r.number_of_guests, 
         o.name, c.business_name, pgh.name;
GO

IF EXISTS (SELECT * FROM sys.views WHERE name = 'VenueRevenueView')
    DROP VIEW VenueRevenueView
GO

CREATE VIEW VenueRevenueView AS
SELECT 
    v.venue_id,
    v.name,
    v.location,
    COUNT(r.booking_id) AS total_bookings,
    SUM(v.cost) AS total_revenue,
    AVG(r.number_of_guests) AS avg_party_size
FROM Venue v
LEFT JOIN Reservation r ON v.venue_id = r.venue_id
GROUP BY v.venue_id, v.name, v.location;
GO

IF EXISTS (SELECT * FROM sys.views WHERE name = 'StaffWorkloadView')
    DROP VIEW StaffWorkloadView
GO

CREATE VIEW StaffWorkloadView AS
SELECT 
    s.employee_id,
    s.name,
    s.role,
    COUNT(rs.booking_id) AS total_assignments,
    COUNT(DISTINCT MONTH(r.date)) AS months_worked
FROM Staff s
LEFT JOIN Reservation_Staff rs ON s.employee_id = rs.staff_id
LEFT JOIN Reservation r ON rs.booking_id = r.booking_id
GROUP BY s.employee_id, s.name, s.role;
GO