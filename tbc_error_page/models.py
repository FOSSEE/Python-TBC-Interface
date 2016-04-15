from django.db import models
import os
import cPickle

def get_json_from_file(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if os.path.isfile(path):
        with  open(path) as json_dump:
            json_data =cPickle.load(json_dump)
            return json_data
    else:
        return False



class Error(models.Model):
    
    chapter_url = models.URLField(max_length = 255)
    number_of_errors = models.IntegerField()
    chapter_name = models.CharField(max_length = 200,)
    is_deliberate = models.IntegerField(default = False)
    
    def create_new_error_data(self, error_json_data):
        # Populates an empty table
        for error_details in error_json_data:
            Error.objects.create(chapter_url = error_details["chapter_urls"],
                                 chapter_name = error_details["chapter_name"],
                                 number_of_errors = int(error_details["number_of_errors"]),
                                 is_deliberate = 0
                                 )

    def delete_redundant_error_data(self, error_json_data):
        # delete errors which have been solved 
        for error_details in error_json_data:
            db_url_list = Error.objects.values_list("chapter_url", flat=True)
            json_url_list = [url_list["chapter_urls"] for url_list in error_json_data]
            c = set(db_url_list)-set(json_url_list) #change variable name.
            for somelist in c:
                Error.objects.filter(chapter_url = somelist).delete()
    
    def update_error_data(self, error_json_data):

        # a little more refined.

        for error_details in error_json_data:
            original_value = Error.objects.get(chapter_url = error_details["chapter_urls"]).number_of_errors
            # if number of errors have increased
            if original_value < error_details["number_of_errors"]:

                Error.objects.filter(chapter_url = error_details["chapter_urls"])\
                .update(number_of_errors = error_details["number_of_errors"],
                        is_deliberate = 0
                        )
            # if number of errors have decreased
            elif original_value > error_details["number_of_errors"]:
                Error.objects.filter(chapter_url = error_details["chapter_urls"])\
                .update(number_of_errors = error_details["number_of_errors"], is_deliberate = 0)
            else:
                # if new errors have been added.
                Error.objects.get_or_create(chapter_url = error_details["chapter_urls"],
                                            number_of_errors = error_details["number_of_errors"]
                                            )

                Error.objects.filter(chapter_url = error_details["chapter_urls"])\
                .update(chapter_url = error_details["chapter_urls"],
                        number_of_errors = error_details["number_of_errors"],
                        chapter_name = error_details["chapter_name"]
                        )




                
    def update_deliberate_error(self, deliberate_error_list):

        for deliberate_urls in deliberate_error_list:
            a = Error.objects.filter(chapter_url = deliberate_urls).update(is_deliberate = 1)
            



class Broken(models.Model):

    broken_url = models.URLField(max_length = 255)
    error_status = models.IntegerField()

    def create_new_broken_data(self, broken_data):
        for broken_details in broken_data:

            Broken.objects.create(broken_url = broken_details["broken_url"],
                                  error_status = broken_details["broken_status"])

    def delete_redundant_broken_data(self, broken_data):
	for broken_details in broken_data:
            db_url_list = Broken.objects.values_list("broken_url", flat=True)
            json_url_list = [url_list["broken_url"] for url_list in broken_data]
            redundant_url = set(db_url_list)-set(json_url_list) #change variable name.
            for delete_url in redundant_url:
                Broken.objects.filter(broken_url = delete_url).delete()


    def update_broken_data(self, broken_data):
	for broken_details in broken_data:

            Broken.objects.get_or_create(broken_url = broken_details["broken_url"],
                                            error_status = broken_details["broken_status"]
                                         )
