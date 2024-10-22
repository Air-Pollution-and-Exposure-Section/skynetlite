InstrumentOnlineHistory = """
CREATE TABLE instrument_online_history (
    instrument_id INTEGER REFERENCES instrument(id),
    online BOOLEAN,
    status_change_time TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    primary key (instrument_id, status_change_time)
);
"""
