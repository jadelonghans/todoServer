import requests
import pytest
import json
import todoserver
"""
   date-fullyear   = 4DIGIT
   date-month      = 2DIGIT  ; 01-12
   date-mday       = 2DIGIT  ; 01-28, 01-29, 01-30, 01-31 based on
                             ; month/year
   time-hour       = 2DIGIT  ; 00-23
   time-minute     = 2DIGIT  ; 00-59
   time-second     = 2DIGIT  ; 00-58, 00-59, 00-60 based on leap second
                             ; rules
   time-secfrac    = "." 1*DIGIT
   time-numoffset  = ("+" / "-") time-hour ":" time-minute
   time-offset     = "Z" / time-numoffset

   partial-time    = time-hour ":" time-minute ":" time-second
                     [time-secfrac]
   full-date       = date-fullyear "-" date-month "-" date-mday
   full-time       = partial-time time-offset

   date-time       = full-date "T" full-time
"""

"""
    Register an event:
    curl -X POST -H "Content-Type: application/json" -d '{"deadline":"1937-01-01T12:00:27.87+00:20", "title":"report", "memo":""}' http://localhost:8080/api/v1/event

    Testcases:
    - Get all event. 200 empty list
    - Get event by index. 404 error
    - valid date registration. 200 with json
    - Invalid date registration. 400 with json
    - Get all event. 200 with one entry
    - get that event by index. 200 with json
    
    Retrieve events:
    curl -X GET http://localhost:8080/api/v1/event
    
    - empty list 

    curl -X GET http://localhost:8080/api/v1/event/2
    -
"""



url = "http://localhost:8080/api/v1/event"

def get_all_empty_test():
    # sending get request and saving the response as response object
    r = requests.get(url)

    assert int(r.status_code) == 200
    # extracting data in json format
    data = r.json()
    assert type(data) is dict
    assert type(data["events"]) is list
    assert len(data["events"]) == 0
    return

def get_event_by_index_empty_test():
    r = requests.get(url + "/1")
    assert int(r.status_code) == 404

    r = requests.get(url + "/-1")
    assert int(r.status_code) == 404
    return

def post_valid_data_test():
    valid_data = {"deadline":"1937-01-01T12:00:27.87+00:20", "title":"report", "memo":""}
    # payload = str.encode(json.dumps(valid_data))

    r = requests.post(url,json=valid_data)
    
    assert int(r.status_code) == 200
    reply = r.json()

    # expected json is {'result': 'success', 'message': 'registered', 'id': 1}
    assert reply['message'] == 'registered'
    assert reply['result'] == 'success'
    return

def post_invalid_data_test():
    valid_data = {"deadline":"1937.01.01T12:00:27.87+00:20", "title":"report", "memo":""}
    
    r = requests.post(url,json=valid_data)
    
    assert int(r.status_code) == 400
    
    reply = r.json()
    # expected json is {'result': 'failure', 'message': 'invalid date format'}
    assert reply['result'] == 'failure'
    return
    
def get_all_test():
    r = requests.get(url)

    assert int(r.status_code) == 200

    data = r.json()
    assert type(data) is dict
    assert type(data["events"]) is list
    assert data["events"] == [{"id": 1, "deadline":"1937-01-01T12:00:27.87+00:20", "title":"report", "memo":""}]
    return

def get_event_by_index():
    r = requests.get(url + "/1")
    assert int(r.status_code) == 200 

    data = r.json()
    print (data)
    assert data == {"id": 1, "deadline":"1937-01-01T12:00:27.87+00:20", "title":"report", "memo":""}
    return

def test_main():
    get_all_empty_test()
    get_event_by_index_empty_test()
    post_valid_data_test()
    post_invalid_data_test()
    get_all_test()
    get_event_by_index()

if __name__ == "__main__":
    # get_all_test()
    post_valid_data_test()
    get_event_by_index()