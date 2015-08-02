import requests

if __name__ == '__main__':
    root = "http://127.0.0.1:5000/"
    print requests.get(root+"things").content
