# -*- coding: utf-8 -*-

import requests
import collections
import os
from urlparse import urljoin



class DisqusCommenting(object):
    """ A class for getting disqus comments per url, also features getting flagged comments."""
  
    base_disqus_url  = "http://disqus.com/api/"


    def check_internet_connection(self):
        """ Checks for the internet connection."""
  
        try:
            requests.get(self.base_disqus_url, timeout = 10)
            self.internet_status = {"status":True, "message": "Connection Passed."}

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.internet_status = {"status": False, "message": "Please Check the internet Connection."}

        return self.internet_status["message"]

    def check_authentication(self, public_key, forum_name, api_version=3.0):

        """ Checks if public key and forum is valid. Returns the public key, forum name for Disqus API."""
        # @TODO - Optional Authentication for read/write/moderate.
        api_version = str(api_version)
        try:
            if self.internet_status["status"] == True:
                url = urljoin(self.base_disqus_url,api_version)+"/forums/details.json" # get a better way to do this. Apparently urljoin doesnt work that way.
                payload = {"api_key":public_key, "forum":forum_name}
                connect_api = requests.get(url, params = payload).json()
  
                if connect_api["code"]== 0:
                    self.public_key = public_key
                    self.forum_name = forum_name
                    self.api_version = api_version
                    self.api_connection_status = {"status": True, "message": "Your api key and forum name are valid."}
                    return self.api_connection_status["message"]
  
                elif connect_api["code"] == 5:
                    self.api_connection_status = {"status": False, "message": "Your api key is invalid."}
                    return self.api_connection_status["message"]

                else:
                    self.api_connection_status = {"status": False, "message": "Your forum name is invalid."}
                    return self.api_connection_status["message"]

            else:
                self.internet_status = {"status": False, "message": "You are still not connected to the internet. Please Check the internet Connection"}
                return self.internet_status["message"]
  
        except AttributeError:
            self.api_connection_status = {"status": False, "message": "Check your internet connection first."}
            return self.api_connection_status["message"]
    
    def get_thread_ids(self):
        """ Returns the counter for thread ids in a forum """
  
        forum_url = urljoin(self.base_disqus_url,self.api_version)+"/forums/listPosts.json" # get a better way to do this. Apparently urljoin doesnt work that way.
        payload = {"api_key":self.public_key,"forum": self.forum_name}
        forum_data = requests.get(forum_url, params=payload).json()
        thread_id_list = [thread_id["thread"] for thread_id in forum_data["response"]]
        counter = collections.Counter(thread_id_list)
        self.counter = counter
        return counter

    def get_comments(self):
        """ Returns the comments and the url of a thread """

        json_like_list = []

        for thread_id in self.counter.keys():   # Find a better way to do this
            comment_list = []
            payload = {"api_key": self.public_key, "thread": thread_id}
            thread_url = urljoin(self.base_disqus_url,self.api_version)+"/threads/list.json" 
            thread_data = requests.get(thread_url, params = payload).json()
            comment_dict = {}
            comment_dict["chapter_urls"] =  thread_data["response"][0]["link"]
            comment_url = urljoin(self.base_disqus_url,self.api_version)+"/threads/listPosts.json" 
            comment_data = requests.get(comment_url, params = payload).json()

            for comments in comment_data["response"]:
                comment_list.append(comments["raw_message"])
            comment_dict["comment_list"] = comment_list


            json_like_list.append(comment_dict)

        return json_like_list


if __name__ == "__main__":
    x = DisqusCommenting()

    y = x.check_internet_connection()
    d = x.check_authentication("enter your disqus api PUBLIC key here", 'enter disqus forum name here ')
    z = x.get_thread_ids()   
    z1 = x.get_comments()

    print z1 # this will print out a json like list of all the urls and the comments on each url
