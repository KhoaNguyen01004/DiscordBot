import datetime
import time
import requests
import json
import os
import random
from deep_translator import GoogleTranslator


class Joke:
    """A random joke generator. Get data from https://official-joke-api.appspot.com"""

    default_url = "https://official-joke-api.appspot.com/random_joke"

    def get_joke_json(self) -> json:
        """
        Description:
        -----------
        Request a random joke 

        Return:
        -------
        A json object of random joke
        """
        return requests.get(self.default_url).json()


class Meme:
    """A random meme generator. Get data from https://api.imgflip.com"""
    default_url = "https://api.imgflip.com/get_memes"
    path = "resources/memes.json"

    def get_meme_json(self):
        """
        Description:
        ------------
        Request a list of Meme and save it as JSON file if the file is not present
        """
        if not os.path.exists(path=self.path):
            os.makedirs('resources')
            with open(file=self.path, mode="w") as write:
                write.write(json.dumps(requests.get(
                    url=self.default_url).json(), indent=4))

    def random_generate(self) -> str:
        """
        Description:
        ------------
        Read the saved memes.json file created by :py:func:`API.Meme.get_meme_json`
        and generate a random meme from the list.
        """
        memes = ""
        with open(file=self.path, mode="r") as read:
            memes = json.load(read)["data"]["memes"]
        return memes[random.randint(0, len(memes))]

    def get_meme(self):
        """
        Description:
        ------------
        Request the meme url and save it as `meme.png` in resources folder
        """
        meme = "resources/meme.png"
        url = self.random_generate()["url"]
        respond = requests.get(url=url)
        if respond.status_code:
            if os.path.exists(path=meme):
                os.remove(path=meme)
            f = open(meme, "wb")
            f.write(respond.content)
            f.close()


class UMD:
    """Handle UMD API. Get data from https://beta.umd.io/"""

    default_url = "https://api.umd.io/v1/"

    def get_courses_list(self) -> json:
        """
        Description:
        ------------
        Get the courses available at UMD in JSON format

        Return:
        -------
        JSON object containing list of courses ID and name
        """
        return requests.get(url=self.default_url + "courses/list").json()

    def get_course_info(self, course_id: str):
        """
        Description:
        ------------
        Request a course info based on given course id

        Return:
        -------
        - A json object containing course information if request successful
        - Error Messages: If the given course ID is invalid or not found
        - None if course is not found through API as well as there is no other related course
        """
        respond = requests.get(url=self.default_url + f"courses/{course_id}")

        if respond.status_code == 200:
            return respond.json()
        else:
            return self.get_related_course_list(course_id=course_id)

    def get_related_course_list(self, course_id: str):
        """
        Description:
        ------------
        Return the courses list with their name related to given course id if there is any

        Return:
        -------
        - The course list if there is any
        - None if there is no course in the list
        """
        respond = self.get_courses_list()
        course_list = list()
        for i in respond:
            if course_id.lower() in i["course"].lower():
                course_list.append(i)
        if len(course_list) > 0:
            return course_list
        else:
            return None


class Weather:
    """Everything I need to implement a weather app. All data is gathered through an API of http://api.openweathermap.org/. I update the structure in near future to support more locations. Currently, this only support Germantown MD, USA and Ho Chi Minh City (VN)"""

    __default_url = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self) -> None:
        """Description:
        ---------------
        Initialize the key to successfully request from Open Weather Map."""
        self.params = {
            "appid": os.environ["openweathermap"]
        }

    def weather_saigon(self):
        """Description:
        ---------------
        Extract info from http://api.openweathermap.org/ to get weather info in Saigon aka Ho Chi Minh City.
        
        Return:
        -------
        - If successfully request: response as json object.
        - If fail request: response's status code, response as string."""
        file_name = "resources/saigon_weather.json"
        if self.update_time():
            self.params["q"] = "Ho Chi Minh City"
            response = requests.get(url=self.__default_url, params=self.params)

            if response.ok:
                with open(file=file_name, mode="w") as f:
                    json.dump(response.json(), f, indent=4)
                return response.json()
            else:
                return response.status_code, response.text
        elif os.path.exists(path=file_name):
            with open(file=file_name, mode="r") as r:
                return json.load(r)

    def weather_germantown(self):
        """Description:
        ---------------
        Extract info from http://api.openweathermap.org/ to get weather info in Germantown MD, USA.
        
        Return:
        -------
        - If successfully request: response as json object.
        - If fail request: response's status code, response as string."""
        file_name = "resources/germantown_weather.json"
        if self.update_time():
            self.params["q"] = "Germantown"
            response = requests.get(url=self.__default_url, params=self.params)

            if response.ok:
                with open(file=file_name, mode="w") as f:
                    json.dump(response.json(), f, indent=4)
                return response.json()
            else:
                return response.status_code, response.text
        elif os.path.exists(path=file_name):
            with open(file=file_name, mode="r") as r:
                return json.load(r)

    def update_time(self):
        """Description:
        ---------------
        This update the time in `time_data.json` file every minute.
        
        Return:
        -------
        True if time has successfully updated, False otherwise"""
        filename = "resources/time_data.json"

        try:
            with open(filename, "r") as file:
                time_data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            time_data = {}

        current_time = time.time()

        # Check if the time data exists and if the difference between the current time and the stored time is 1 minute or more
        if "stored_time" in time_data and (current_time - time_data["stored_time"]) < 60:
            return False
        else:
            # Update the time data dictionary with the current time
            time_data["stored_time"] = current_time

            # Write the time data to the JSON file
            with open(filename, "w") as file:
                json.dump(time_data, file)

            return True

    def get_temp(self, obj: json):
        """Description:
        ---------------
        Get the temperature information."""
        if obj == None:
            return None
        data = obj["main"]
        temp = {}
        temp["average"] = self.k_to_c(float(data["temp"]))
        temp["feels_like"] = self.k_to_c(float(data["feels_like"]))
        temp["temp_max"] = self.k_to_c(float(data["temp_max"]))
        temp["temp_min"] = self.k_to_c(float(data["temp_min"]))
        return temp

    def get_description(self, obj: json):
        """Description:
        ---------------
        Get a brief description of current weather"""
        return obj["weather"][0]["description"]

    def get_sun_info(self, obj: json):
        """Description:
        ---------------
        Get what time is sunrise and sunset
        {"sunrise": data, "sunset": data}"""
        data = {}
        data["sunrise"] = self.time_convert(obj["sys"]["sunrise"])
        data["sunset"] = self.time_convert(obj["sys"]["sunset"])
        return data

    def get_date(self, obj: json):
        return self.time_convert(obj["dt"])

    def time_convert(self, unix_timestamp: int) -> str:
        """Description:
        ---------------
        Return a human readable string from given unix timestamp"""
        dt_object = datetime.datetime.fromtimestamp(unix_timestamp)
        return dt_object.strftime('%Y-%m-%d %H:%M:%S')

    def k_to_c(self, degree: float):
        return round(degree - 273.15, ndigits=1)

    def en_to_vi(self, text):
        """Description:
        ---------------
        Translate text from English to Vietnamese"""
        return GoogleTranslator(source='en', target='vi').translate(text)

    def timezone(self, obj: json):
        return int(obj["timezone"]/3600)
