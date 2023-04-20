import requests
import os.path
import time
import datetime

from gtmetrix import settings
from gtmetrix.exceptions import *
from gtmetrix.utils import  (validate_email,
                             validate_api_key)

__all__ = ['GTmetrixInterface',]


class _TestObject(object):
    """GTmetrix Test representation."""
    STATE_QUEUED = 'queued'
    STATE_STARTED = 'started'
    STATE_COMPLETED = 'completed'
    STATE_ERROR = 'error'

    def __init__(self, auth, test_id, poll_state_url=None, credits_left=None):
        self.poll_state_url = (poll_state_url or
                               os.path.join(settings.GTMETRIX_REST_API_URL, test_id))
        self.test_id = test_id
        self.credits_left = credits_left
        self.state = self.STATE_QUEUED
        self.credits_left = 0
        self.auth = auth
        self.results = {}
        self.resources = {}
        self.pagespeed_score = {}
        self.yslow_score = {}
        self.page_bytes = {}
        self.page_load_time = {}
        self.page_elements ={}
        self.pagespeed_url ={}
        self.yslow_url = {}
        self.api_data = {}
        self.list_pagespeed_issues = []
        self.list_yslow_issues = []

    def _request(self, url):
        response = requests.get(url, auth=self.auth)
        response_data = response.json()

        if response.status_code == 404:
            raise GTmetrixTestNotFound(response_data['error'])

        if response.status_code == 400:
            raise GTmetrixInvalidTestRequest(response_data['error'])

        if response.status_code == 402:
            raise GTmetrixMaximumNumberOfApis(response_data['error'])

        if response.status_code == 429:
            raise GTmetrixManyConcurrentRequests(response_data['error'])

        return response_data

    def fetch_results(self):
        """Get the test state and results/resources (when test complete)."""
        response_data = self._request(self.poll_state_url)
        number_executions = 0
        while not self.state == self.STATE_COMPLETED and (number_executions < 30):
            number_executions += 1
            time.sleep(30)
            response_data = self._request(self.poll_state_url)
            self.state = response_data['state']
        self._extract_results(response_data)

        return self.api_data

    def _get_result( self, key, dflt='' ):
      return self.results[ key ] if key in self.results else dflt
  
    def _get_resources(self,key,dflt=''):
      return self.resources[ key ] if key in self.resources else dflt

    def _extract_results(self, response_data):
      if 'results' in response_data:
        self.results = response_data['results']
        self.pagespeed_score = self._get_result( 'pagespeed_score' )
        self.yslow_score = self._get_result( 'yslow_score' )
        self.page_bytes = self._get_result( 'page_bytes' )
        self.page_load_time = self._get_result( 'fully_loaded_time' )
        self.page_elements = self._get_result('page_elements')

      if 'resources' in response_data:
        self.resources = response_data['resources']
        self.pagespeed_url = self._get_resources( 'pagespeed' )
        self.yslow_url = self._get_resources( 'yslow' )
    
      self.api_data = {'pagespeed_score':self.pagespeed_score,'yslow_score':self.yslow_score,'total_page_size':self.page_bytes,'fully_loaded_time':self.page_load_time,
             'requests':self.page_elements,'pagespeed_url':self.pagespeed_url,'yslow_url':self.yslow_url}



class GTmetrixInterface(object):
    """Provides an interface to access GTmetrix REST API."""
    def __init__(self, user_email=None, api_key=None):
        # Validate and set instance variables
        self.set_auth_email_and_key(user_email, api_key)
        self.auth = (self.user_email, self.api_key)

    def set_auth_email_and_key(self, user_email=None, api_key=None):
        # Get from params or default to values from settings
        self.user_email = user_email or settings.GTMETRIX_REST_API_EMAIL
        self.api_key = api_key or settings.GTMETRIX_REST_API_KEY

        # Make sure they're valid
        self.validate_user_email()
        self.validate_api_key()

    def validate_user_email(self):
        """Hook for user email validation."""
        return validate_email(self.user_email)

    def validate_api_key(self):
        """Hook for api key validation."""
        return validate_api_key(self.api_key)

    def start_test(self, url, location_id,**data):
        """ Start a Test """
        data.update({'url': url,'location':location_id})
        response = requests.post(settings.GTMETRIX_REST_API_URL, data=data, auth=self.auth)
        response_data = response.json()

        if response.status_code != 200:
            raise GTmetrixInvalidTestRequest(response_data['error'])

        return _TestObject(self.auth, **response_data)
    
    
class IdentifyingPageSpeedIssues(GTmetrixInterface):

  def fetch_results(self,pagespeed_resource_url):
    """Here we are making list of Issues which slowing down Pagespeed"""
    data = []
    response = requests.get(pagespeed_resource_url,auth=self.auth)
    response_data = response.json()

    if response.status_code != 200:
        raise GTmetrixInvalidTestRequest(response_data['error'])
    for pagespeed_issues in response_data['rules']:
        if('score' in pagespeed_issues.keys()):
          if(int(pagespeed_issues['score']) < 90):
              data.append(pagespeed_issues['name'])
    return(','.join(data))

  
class IdentifyingYslowIssues(GTmetrixInterface):

  def fetch_results(self,pagespeed_resource_url):
    """Here we are makinglist of Yslow Issues"""
    data = []
    response = requests.get(pagespeed_resource_url,auth=self.auth)
    response_data = response.json()

    if response.status_code != 200:
        raise GTmetrixInvalidTestRequest(response_data['error'])
      
    Yslow_speed_issues = response_data['g']
    for value in Yslow_speed_issues.values():
      if('score' in value.keys()):
          if(int(value['score']) < 90):
            data.append(value['message'])
    return(','.join(data))
