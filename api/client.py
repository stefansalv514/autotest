#import requests


#class navigatorClient:

 #   _s = requests.session()
  #  host = None

   # def __init__(self, host):
    #    self.host = host
    #def login(self, username, password, grant_type, client_id, client_secret):
      #  data = {"username": username, "password": password, "grant_type": grant_type, "client_id": client_id, "client_secret": client_secret}
     #   return self._s.post(self.host + "/auth", data)

  #  def authorize(self, username, password, grant_type, client_id, client_secret):
   #     res = self.login(username, password, grant_type, client_id, client_secret)
    #    if res.status_code != 200:
      #      raise Exception("Unable to authorize using given credentials")
      #  session_token = res.json().get("token")
       # cookie = requests.cookies.create_cookie("token", session_token)
        #self._s.cookies.set_cookie(cookie)