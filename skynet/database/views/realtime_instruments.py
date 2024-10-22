realtime_instruments= """
CREATE VIEW realtime_instruments AS
SELECT instrument.id AS instrument_id, 
       instrument.manufacturer, 
       instrument.name, 
       instrument.model, 
       instrument.type, 
       instrument.serial_number, 
       instrument.mac_address, 
       instrument.software_version, 
       instrument.owner_email, 
       instrument.associated_email, 
       instrument.label, 
       instrument.latitude, 
       instrument.longitude, 
       instrument.device_location_type, 
       instrument.online, 
       instrument.ip_address, 
       instrument.wifi_password, 
       instrument.sim_number, 
       instrument.phone_number, 
       instrument.imei_number, 
       foo.last_report_date
FROM instrument
LEFT JOIN (
    SELECT instrument_id, MAX(date) AS last_report_date
    FROM temperature
    GROUP BY instrument_id
) AS foo ON instrument.id = foo.instrument_id
WHERE instrument.manufacturer IN ('Purple Air', 'Wicked Device')
ORDER BY instrument.id ASC;
"""
