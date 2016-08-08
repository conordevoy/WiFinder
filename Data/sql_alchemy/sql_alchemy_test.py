class Room(db.Model):
    room_id = db.Column(db.String, primary_key=True)
    capacity = db.Column(db.Integer)
    building = db.Column(db.String)
    campus = db.Column(db.String)

    def __init__(self, room_id, capacity, building, campus):
        self.room_id = room_id
        self.capacity = capacity
        self.building = building
        self.campus = campus

    def __repr__(self):
        return '<Room %r' % self.room_id

class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    room = db.Column(db.String)
    module = db.Column(db.String)
    registered_students = db.Column(db.Integer)

    def __init__(self, class_id, hour, datetime, room, module, registered_students):
        self.class_id = class_id
        self.hour = hour
        self.datetime = datetime
        self.room = room
        self.module = module
        self.registered_students = registered_students

    def __repr__(self):
        return '<Class %r' % self.class_id

class wifi_logs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    hour = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    room = db.Column(db.String)
    log_count = db.Column(db.String)
    class_id = db.Column(db.String)

    def __init__(self, log_id, time, hour, datetime, room, log_count, class_id):
        self.log_id = log_id
        self.time = time
        self.hour = hour
        self.datetime = datetime
        self.room = room
        self.log_count = log_count
        self.class_id = class_id

    def __repr__(self):
        return '<Log %r' % self.log_id

class occupancy(db.Model):
    occupancy_id = db.Column(db.Int, primary_key=True)
    hour = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    room = db.Column(db.String)
    occupancy = db.Column(db.Integer)
    class_id = db.Column(db.String)

    def __init__(self, occupancy_id, hour, datetime, room, occupancy, class_id):
        self.occupancy_id = occupancy_id
        self.hour = hour
        self.datetime = datetime
        self.room = room
        self.occupancy = occupancy
        self.class_id = class_id

    def __repr__(self):
        return '<Occupancy %r' % self.occupancy_id
    