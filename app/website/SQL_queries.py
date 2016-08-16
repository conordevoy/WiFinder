

get_all_hours = "SELECT DISTINCT Hour FROM CLASS;"
get_all_rooms = "SELECT DISTINCT RoomID FROM ROOM;"
get_all_modules = "SELECT DISTINCT Module FROM CLASS;"
get_all_dates = "SELECT DISTINCT Datetime FROM CLASS;"


get_average_counts_room_date_time = """
                            SELECT Avg(Log_Count) as count
                            FROM WIFI_LOGS
                            WHERE Room = "{room}"
                            AND Datetime = "{date}"
                            AND strftime('%H', Time) = "{hour}"
                            """


weekly_occupancy_query = """
                            SELECT AVG(Log_Count) as count, Datetime as date
                            FROM WIFI_LOGS
                            WHERE strftime('%W', Datetime) =  strftime('%W', "{date}")
                            AND strftime('%H', Time) BETWEEN "09" and "17"
                            AND strftime('%w', Datetime) BETWEEN "1" and "5"
                            And Room = "{room}"
                            GROUP BY ClassID
                            ORDER BY date DESC
                            """


average_room_occupancy_query = """
                            Select AVG(Occupancy)
                            FROM OCCUPANCY
                            WHERE Hour BETWEEN "9" and "17"
                            AND strftime('%w', Datetime) BETWEEN "1" and "5"
                            AND Room = "{room}"
                            """


day_count_query = """select AVG(Log_Count) as count
                            from WIFI_LOGS
                            where Room = "{room}"
                            and Datetime = "{date}"
                            AND strftime('%H', Time) BETWEEN "09" and "17"
                            GROUP BY ClassID"""


day_count_and_survey_query = """select Avg(w.Log_Count) as count, o.Occupancy as survey, o.Hour as hour
                                        from WIFI_LOGS w JOIN OCCUPANCY o
                                        where w.Room = "{room}"
                                        and w.Datetime = "{date}"
                                        AND strftime('%H', w.Time) BETWEEN "09" and "17"
                                        and o.ClassID = w.ClassID
                                        GROUP BY w.hour
                                        ORDER BY w.hour ASC
                                        """
