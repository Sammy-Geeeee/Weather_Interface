// Weather Interface

// This program is a Console based weather program
// Input is a location and what type of output you want, and the output would be the weather information


using static System.Console;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;


namespace Weather_Interface
{
    internal class Program
    {
        static void Main(string[] args)
        {           
            IConfiguration config = new ConfigurationBuilder()  // This will add all the environmental variables from the appsetting.json file
                .AddJsonFile("appsettings.json")
                .AddEnvironmentVariables()
                .Build();
            
            var key = config.GetValue<String>("openweathermap_key");  // This will retrieve the weather api key

            while (true)  // To loop this program forever
            {
                WriteLine("\nWhere would you like the weather for? 'Quit' to exit. ");
                string location = ReadLine();
                if (location.ToLower() == "quit")  // Allows you to break the loop
                {
                    break;
                }

            // Need to declare these so they can be used outside the try block
            string[] coords;
            dynamic data;

                try
                {
                    coords = latLongInfo(location, key);  // This will find the coordinates of the location you want
                    data = weatherData(coords, key);  // This will find the weather data of the location you want
                }
                catch (Exception e)  // An exception will occur if the location url cannot be found
                {
                    WriteLine("Invalid location. Please try again");
                    continue;
                }
                
                WriteLine("\nWhat kind of information would you like? 'Current', 'Daily', 'Hourly'. ");
                string data_type = ReadLine();
                if (data_type.ToLower() == "current")
                {
                    currentWeatherInfo(data, coords[2]);
                }
                else if (data_type.ToLower() == "daily")
                {
                    dailyWeatherInfo(data, coords[2]);
                }
                else if (data_type.ToLower() == "hourly")
                {
                    hourlyWeatherInfo(data, coords[2]);
                }
                else
                {
                    WriteLine("\nYou need a valid weather data type. Please try again. ");
                    continue;
                }
            }
        }


        static DateTime unixToDateTime(long unix_time)
        {
            // This function is just to find the datetime from the unix datetime
            DateTime date_time = new DateTime(1970, 1, 1, 0, 0, 0, 0, System.DateTimeKind.Utc);
            date_time = date_time.AddSeconds(unix_time).ToLocalTime();
            return date_time;
        }


        static string timeShift(int unix_time, int locale_offset, string time_format="")
        {
            // This function will return the correct time in the correct format
            int auckland_offset = 13*60*60;  // This is the offset from UTC time in seconds, needs to be 13 during DST, 12 otherwise
            int total_offset = -auckland_offset + locale_offset;
            DateTime local_time = unixToDateTime(unix_time + total_offset);  // Turns the seconds into a datetime object
            if (time_format == "hourly")
            {
                return local_time.ToString("dddd HH:mm");
            }
            else if (time_format == "daily")
            {
                return local_time.ToString("MMMM dd");
            }
            else if (time_format == "current")
            {
                return local_time.ToString("dddd, dd MMMM - HH:mm");
            }
            else
            {
                return "Invalid Time Format. Try again";
            }
        }


        static string[] latLongInfo(string location, string api_key)
        {
            // This function is to return an array of the latitude, longitude, and location name of the requested area
            var url = $"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}";  // To create the url we need to use

            var httpClientHandler = new HttpClientHandler();  // These lines will create all the http reading parts
            var httpClient = new HttpClient(httpClientHandler)
            {
                BaseAddress = new Uri(url)
            };
            
            using (var response = httpClient.GetAsync(url))  // This will retrieve the info at the url
            {
                var data_str = response.Result.Content.ReadAsStringAsync().Result;  // This returns the result as a string of json data
                dynamic data_json = JsonConvert.DeserializeObject(data_str);  // This will convert the string to json format again
                
                string lat = data_json["coord"]["lat"];
                string lon = data_json["coord"]["lon"];
                string location_name = $"{data_json["name"]}, {data_json["sys"]["country"]}";
                string[] data = {lat, lon, location_name};
                return data;
            }
        }


        static dynamic weatherData(string[] coordinates, string api_key)
        {
            // This function will return all the json data for the weather of a certain location
            var url = $"https://api.openweathermap.org/data/2.5/onecall?lat={coordinates[0]}&lon={coordinates[1]}&appid={api_key}";  // To create the url we need to use

            var httpClientHandler = new HttpClientHandler();  // These lines will create all the http reading parts
            var httpClient = new HttpClient(httpClientHandler)
            {
                BaseAddress = new Uri(url)
            };
            
            using (var response = httpClient.GetAsync(url))  // This will retrieve the info at the url
            {
                var data_str = response.Result.Content.ReadAsStringAsync().Result;  // This returns the result as a string of json data
                dynamic data_json = JsonConvert.DeserializeObject(data_str);  // This will convert the string to json format again
                return data_json;
            }
        } 
    
    
        static void currentWeatherInfo(dynamic all_data, string location)
        {
            // This location is to print all the current weather info for the given location
            var data = all_data["current"];
            var time = timeShift(Int32.Parse(data["dt"].ToString()), Int32.Parse(all_data["timezone_offset"].ToString()), "current");
            var weather = $"{data["weather"][0]["main"]} - {data["weather"][0]["description"]}";
            var temp_actual = data["temp"] - 273.15;
            var temp_perceived = data["feels_like"] - 273.15;
            var humidity = data["humidity"];
            var cloudiness = data["clouds"];
            var wind_speed = data["wind_speed"] * 3.6;

            WriteLine($"\nCurrent Weather Information - {location}");
            WriteLine($"    {time}");
            WriteLine($"    {weather}");
            WriteLine($"    Temperature: {temp_actual:f1}°C");
            WriteLine($"    Feels like: {temp_perceived:f1}°C");
            WriteLine($"    Humidity: {humidity}%");
            WriteLine($"    Cloud Cover: {cloudiness}%");
            WriteLine($"    Wind Speed: {wind_speed:f0} km/h");
        }


        static void dailyWeatherInfo(dynamic all_data, string location)
        {
            // This location is to print all the daily weather info for the given location
            var data = all_data["daily"];
            Newtonsoft.Json.Linq.JObject[] daily_weather = {data[1], data[2], data[3], data[4], data[5], data[6], data[7]};
            WriteLine($"\nDaily Weather Information - {location}");

            foreach (var day in daily_weather)
            {
                var time = timeShift(Int32.Parse(day["dt"].ToString()), Int32.Parse(all_data["timezone_offset"].ToString()), "daily");
                var weather = $"{day["weather"][0]["main"]} - {day["weather"][0]["description"]}";
                var rain_chance = float.Parse(day["pop"].ToString()) * 100;
                var temp = float.Parse(day["temp"]["day"].ToString()) - 273.15;
                var temp_min = float.Parse(day["temp"]["min"].ToString()) - 273.15;
                var temp_max = float.Parse(day["temp"]["max"].ToString()) - 273.15;
                var humidity = float.Parse(day["humidity"].ToString());
                var cloudiness = day["clouds"];
                var wind_speed = float.Parse(day["wind_speed"].ToString()) * 3.6;
                
                WriteLine($"    {time}");
                WriteLine($"    {weather}");
                WriteLine($"    Rain Chance: {rain_chance:f0}%");
                WriteLine($"    Temperature: {temp:f1}°C");
                WriteLine($"    Max. Temperature: {temp_max:f1}°C");
                WriteLine($"    Min. Temperature: {temp_min:f1}°C");
                WriteLine($"    Humidity: {humidity}%");
                WriteLine($"    Cloud Cover: {cloudiness}%");
                WriteLine($"    Wind Speed: {wind_speed:f0}km/h\n");
            }

        }


        static void hourlyWeatherInfo(dynamic all_data, string location)
        {
            // This location is to print all the hourly weather info for the given location
            var data = all_data["hourly"];
            List<Newtonsoft.Json.Linq.JObject> hourly_weather = new List<Newtonsoft.Json.Linq.JObject>();
            WriteLine($"\nHourly Weather Information - {location}");
            
            foreach (var i in Enumerable.Range(1, 24+1))
            {
                hourly_weather.Add(data[i]);
            }

            foreach (var hour in hourly_weather)
            {
                var time = timeShift(Int32.Parse(hour["dt"].ToString()), Int32.Parse(all_data["timezone_offset"].ToString()), "hourly");
                var weather = $"{hour["weather"][0]["main"]} - {hour["weather"][0]["description"]}";
                var rain_chance = float.Parse(hour["pop"].ToString()) * 100;
                var temp = float.Parse(hour["temp"].ToString()) - 273.15;
                var humidity = float.Parse(hour["humidity"].ToString());
                var cloudiness = float.Parse(hour["clouds"].ToString());
                var wind_speed = float.Parse(hour["wind_speed"].ToString()) * 3.6;

                WriteLine($"    {time}");
                WriteLine($"    {weather}");
                WriteLine($"    Rain Chance: {rain_chance:f0}%");
                WriteLine($"    Temperature: {temp:f1}°C");
                WriteLine($"    Humidity: {humidity}%");
                WriteLine($"    Cloud Cover: {cloudiness}%");
                WriteLine($"    Wind Speed: {wind_speed:f0}km/h\n");
            }
        }
    }
}
