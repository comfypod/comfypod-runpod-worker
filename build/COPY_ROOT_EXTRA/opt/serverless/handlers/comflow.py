import json
import requests
import datetime
import time
import os
import base64

from handlers.basehandler import BaseHandler

"""
Handler classes are generally bound to a specific workflow file.
To modify values we have to be confident in the json structure.

One exception - RawWorkflow will send payload['workflow_json'] to the ComfyUI API after
downloading any URL's to the input directory and replacing the URL with a local path.
"""


class Comflow(BaseHandler):
    ENDPOINT_CHECK = "http://127.0.0.1:18188/prompt"

    WORKFLOW_FILE = None

    def __init__(self, payload, workflow_json=None):
        super().__init__(payload, workflow_json)
        # override the default endpoint
        self.ENDPOINT_PROMPT = "http://127.0.0.1:18188/comflow/run"

    def set_prompt(self):
        self.prompt = self.payload

    def get_s3_settings(self):        
        settings = {}
        settings["aws_access_key_id"] = "none"
        settings["aws_secret_access_key"] = "none"
        settings["aws_endpoint_url"] = "https://example.com"
        settings["aws_bucket_name"] = "none"
        settings["connect_timeout"] = 5
        settings["connect_attempts"] = 1
        return settings
    
    def is_server_ready(self):
        try:
            req = requests.head(self.ENDPOINT_CHECK)
            return True if req.status_code == 200 else False
        except:
            return False   

    def get_result(self, job_id):
        self.job_time_completed = datetime.datetime.now()
        self.result = {
            "timings": {
                "job_time_received": self.job_time_received.ctime(),
                "job_time_queued": self.job_time_queued.ctime(),
                "job_time_processed": self.job_time_processed.ctime(),
                "job_time_completed": self.job_time_completed.ctime(),
                "job_time_total": (self.job_time_completed - self.job_time_received).seconds
          }
        }
        return self.result
             

"""
Example Request Body:

{
  "input": {
    "status_endpoint": "https://webhook.site/4e4212eb-09b7-4264-9dc2-18daef4d19d7/api/update-run",
    "file_upload_endpoint": "https://webhook.site/4e4212eb-09b7-4264-9dc2-18daef4d19d7/api/file-upload",
    "webhook_url": "https://webhook.site/4e4212eb-09b7-4264-9dc2-18daef4d19d7/webhook",
    "workflow_api": {
      "2": {
        "inputs": {
          "images": [
            "4",
            0
          ],
          "filename_prefix": "ComfyUI"
        },
        "class_type": "SaveImage"
      },
      "4": {
        "inputs": {
          "input_id": "https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/3211ef8e-bec9-45c0-987b-6841f121c47a/width=1536,quality=90/00008-2506650012.jpeg"
        },
        "class_type": "ComflowInputImage"
      }
    }
  }
}

"""
