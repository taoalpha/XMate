MAT: 1A
HOST: http://polls.apiblueprint.org/

# cs5412

This is the api doc for cs5412: cloud computing class, group xmate.

## User Collection [/user]

### List profile of a specific user [GET]

+ Response 200 (application/json)
    + Headers
    
            Location: /user/_fbid_
    + Body
        
            {
                "status":1,
                "_id": "18a9sd89as08d90as8d9",
                "username": "tao",
                "FacebookID": 8a7sd80as7d90a8df908asf,
								"age": 19,
								"gender": "male",
                "preferred": "male",
								"city": "ithaca",
								"latitude": 182.9,
								"longitude": 129.0,
								"credits": 10,
								"height":170,
								"weight":200,
                "conflict_list": [],
                "schedule_list": [],
                "history_events": [],
                "history_partner": [],
                "unprocessed_message": [],
                "joinTime": 146242424.0
            }


### Create a New User [POST]

You may create the user by sending a post to the api.

+ Request (application/json)

    + Headers

            Location: /user

    + Body

            {
                "FacebookID": 8a7sd80as7d90a8df908asf,
                "username": "tao",
								"age": 19,
								"gender": "male",
								"latitude": 182.9,
								"longitude": 129.0,
								"height":170,
								"weight":200
            }


### Update User Information [PUT]

You may update the user by sending a post to the api with put method.

+ Request (application/json)

    + Headers

            Location: /user/_id_
            
    + Body
    
            {
                "preferred": "female"
            }

+ Response 201 (application/json)

    + Body

            {
                "status":1,
                "msg": "updated successfully"
            }


## Schedule Collection [/schedule]


### List profile of a specific schedule [GET]

List the profile of a specific schedule.

+ Request (application/json)
    + Headers

            Location: /schedule/_id_
            
    + Body
    
            {
                "type": "lol"
            }

+ Response 200 (application/json)
        
        {
            "status":1,
            "_id": "18a9sd89as08d90as8d9",
            "owner": "8a7sd89as7d86a78d6as",
            "type": "running",
            "member": [],
            "start_time": 146242424.0,
            "end_time": 146242424.0,
            "address_lo": 123.9,
            "address_la": 111.0,
            "address_name": "ithaca",
            "created_time": 146242424.0
        }

List the matches for a schedule:

+ Request (application/json)
    + Headers

            Location: /schedule/_id_/match
            
    + Body
    
            {}

+ Response 200 (application/json)
        
        {
            "status":1,
						"matches": []
        }



### Create a New Schedule [POST]

You may create the schedule by sending a post to the api.

+ Request (application/json)
		+ Headers

            Location: /schedule

	  + Body

        		{
        		    "owner": "1293890128sdad098",
        		    "type": "running",
        		    "start_time": 146242424.0,
        		    "end_time": 146242424.0,
        		    "address_lo": 123.9,
        		    "address_la": 111.0,
        		    "address_name": "ithaca"
        		}

+ Response 201 (application/json)
 
    + Body

            {
                "status":1,
                "msg": "updated successfully"
            }

### Update Schedule Information [PUT]

You may create the user by sending a post to the api.

+ Request (application/json)
    + Headers

            Location: /schedule/_id_
            
    + Body
    
            {
                "type": "lol"
            }

+ Response 201 (application/json)

    + Headers

            Location: /schedule/_fbid_

    + Body

            {
                "status":1,
                "msg": "updated successfully"
            }

