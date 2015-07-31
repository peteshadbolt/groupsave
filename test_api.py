import requests

def test_list():
    output = requests.get("http://localhost:5000/todos")
    print output.content

if __name__ == '__main__':
    import nose
    nose.main()

