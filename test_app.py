from app import app


#first positive test case
def test_hello_route_sucsess():
    tester=app.test_client
    responce=tester.get('/hello')

    assert responce.status_code==200




# #first failed test case
# def test_hello_route_failure():
#     tester=app.test_client
#     response=tester.get('/hello')

#     assert response.status_code==500






def test_hello_route_sucsess():
    tester=app.test_client()
    data = {"gestation":[236],
                    "parity":[0],
                    "age":[34],
                    "height":[74],
                    "weight":[90],
                    "smoke":[0]
                    }

    response=tester.post("/predict",json=data)

    assert response.status_code==200


def test_hello_route_invalid_data():
        tester=app.test_client()
        data = {"gestation":['236'],
                    "parity":[0],
                    "age":[34],
                    "height":[74],
                    "weight":[90],
                    "smoke":[0]
                    }

        response=tester.post("/predict",json={})

        assert response.status_code==500


def test_hello_route_wrong_url():
    tester=app.test_client()
    data = {"gestation":[236],
                    "parity":[0],
                    "age":[34],
                    "height":[74],
                    "weight":[90],
                    "smoke":[0]
                    }

    response=tester.post("/oredict",json=data)

    assert response.status_code==404



def test_hello_route_wrong_method():
        tester=app.test_client()
        data = {"gestation":[236],
                    "parity":[0],
                    "age":[34],
                    "height":[74],
                    "weight":[90],
                    "smoke":[0]
                    }

        response=tester.get("/predict",json=data)

        assert response.status_code==405