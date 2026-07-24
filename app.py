from flask import Flask,render_template,request
from datetime import datetime
import requests
from database import init_db ,save_weather , get_history
app = Flask(__name__)

API_KEY ="8730b6fbd0dd8fc7d9d077e5049ed68d"
BASE_URL ="https://api.openweathermap.org/data/2.5/forecast"


PREFECTURE_NAMES = {
    "Hokkaido": "北海道",
    "Aomori": "青森県",
    "Iwate": "岩手県",
    "Miyagi": "宮城県",
    "Akita": "秋田県",
    "Yamagata": "山形県",
    "Fukushima": "福島県",
    "Ibaraki": "茨城県",
    "Tochigi": "栃木県",
    "Gunma": "群馬県",
    "Saitama": "埼玉県",
    "Chiba": "千葉県",
    "Tokyo": "東京都",
    "Kanagawa": "神奈川県",
    "Niigata": "新潟県",
    "Toyama": "富山県",
    "Ishikawa": "石川県",
    "Fukui": "福井県",
    "Yamanashi": "山梨県",
    "Nagano": "長野県",
    "Gifu": "岐阜県",
    "Shizuoka": "静岡県",
    "Aichi": "愛知県",
    "Mie": "三重県",
    "Shiga": "滋賀県",
    "Kyoto": "京都府",
    "Osaka": "大阪府",
    "Hyogo": "兵庫県",
    "Nara": "奈良県",
    "Wakayama": "和歌山県",
    "Tottori": "鳥取県",
    "Shimane": "島根県",
    "Okayama": "岡山県",
    "Hiroshima": "広島県",
    "Yamaguchi": "山口県",
    "Tokushima": "徳島県",
    "Kagawa": "香川県",
    "Ehime": "愛媛県",
    "Kochi": "高知県",
    "Fukuoka": "福岡県",
    "Saga": "佐賀県",
    "Nagasaki": "長崎県",
    "Kumamoto": "熊本県",
    "Oita": "大分県",
    "Miyazaki": "宮崎県",
    "Kagoshima": "鹿児島県",
    "Okinawa": "沖縄県"
}
CITY_MAP = {
    "北海道": "Hokkaido",
    "青森": "Aomori",
    "青森県": "Aomori",
    "岩手": "Iwate",
    "岩手県": "Iwate",
    "宮城": "Miyagi",
    "宮城県": "Miyagi",
    "秋田": "Akita",
    "秋田県": "Akita",
    "山形": "Yamagata",
    "山形県": "Yamagata",
    "福島": "Fukushima",
    "福島県": "Fukushima",
    "茨城": "Ibaraki",
    "茨城県": "Ibaraki",
    "栃木": "Tochigi",
    "栃木県": "Tochigi",
    "群馬": "Gunma",
    "群馬県": "Gunma",
    "埼玉": "Saitama",
    "埼玉県": "Saitama",
    "千葉": "Chiba",
    "千葉県": "Chiba",
    "東京": "Tokyo",
    "東京都": "Tokyo",
    "神奈川": "Kanagawa",
    "神奈川県": "Kanagawa",
    "新潟": "Niigata",
    "新潟県": "Niigata",
    "富山": "Toyama",
    "富山県": "Toyama",
    "石川": "Ishikawa",
    "石川県": "Ishikawa",
    "福井": "Fukui",
    "福井県": "Fukui",
    "山梨": "Yamanashi",
    "山梨県": "Yamanashi",
    "長野": "Nagano",
    "長野県": "Nagano",
    "岐阜": "Gifu",
    "岐阜県": "Gifu",
    "静岡": "Shizuoka",
    "静岡県": "Shizuoka",
    "愛知": "Aichi",
    "愛知県": "Aichi",
    "三重": "Mie",
    "三重県": "Mie",
    "滋賀": "Shiga",
    "滋賀県": "Shiga",
    "京都": "Kyoto",
    "京都府": "Kyoto",
    "大阪": "Osaka",
    "大阪府": "Osaka",
    "兵庫": "Hyogo",
    "兵庫県": "Hyogo",
    "奈良": "Nara",
    "奈良県": "Nara",
    "和歌山": "Wakayama",
    "和歌山県": "Wakayama",
    "鳥取": "Tottori",
    "鳥取県": "Tottori",
    "島根": "Shimane",
    "島根県": "Shimane",
    "岡山": "Okayama",
    "岡山県": "Okayama",
    "広島": "Hiroshima",
    "広島県": "Hiroshima",
    "山口": "Yamaguchi",
    "山口県": "Yamaguchi",
    "徳島": "Tokushima",
    "徳島県": "Tokushima",
    "香川": "Kagawa",
    "香川県": "Kagawa",
    "愛媛": "Ehime",
    "愛媛県": "Ehime",
    "高知": "Kochi",
    "高知県": "Kochi",
    "福岡": "Fukuoka",
    "福岡県": "Fukuoka",
    "佐賀": "Saga",
    "佐賀県": "Saga",
    "長崎": "Nagasaki",
    "長崎県": "Nagasaki",
    "熊本": "Kumamoto",
    "熊本県": "Kumamoto",
    "大分": "Oita",
    "大分県": "Oita",
    "宮崎": "Miyazaki",
    "宮崎県": "Miyazaki",
    "鹿児島": "Kagoshima",
    "鹿児島県": "Kagoshima",
    "沖縄": "Okinawa",
    "沖縄県": "Okinawa"
}
def get_icon(weather_text):
    if "雨" in weather_text: 
        return "☂" 
    elif "曇" in weather_text: 
        return "☁" 
    elif "晴" in weather_text: 
        return "☀" 
    else: return ""


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        forecast_list = data["list"]

        daily_forecast = []

        for item in forecast_list:
            if "12:00:00" in item["dt_txt"]:
                weather =item["weather"][0]["description"]
                if "雨" in weather:
                    icon = "☔"
                elif "雲" in weather or "曇"in weather:
                    icon ="☁️"
                elif "晴" in weather:
                    icon ="☀️"
                else:
                    icon =""
                daily_forecast.append({
                    "date": item["dt_txt"][5:10],
                    "temp":round(item["main"]["temp"]),
                    "icon":icon
                })
        forecast =[]
        for item in forecast_list[:8]:
            weather = item["weather"][0]["description"]
            if "雨" in weather:
                icon = "☔"
            elif "曇" in weather or "雲"in weather:
                icon ="☁️"
            elif "晴"in weather:
                icon = "☀️"
            else:
                 icon =""
                
            forecast.append({
                "time": item["dt_txt"][11:16],
                "temp":round(item["main"]["temp"]),
                "icon":icon
            })

        temps = [item["main"]["temp"] for item in forecast_list]
        max_temp = max(temps)
        min_temp = min(temps)

        weather_text = forecast_list[0]["weather"][0]["description"]

        def weather_label(text):

            if "雨" in text:
                return "雨"
            elif "曇" in text or "雲" in text:
                return "曇り"
            elif "晴" in text:
                return "晴れ"
            else:
                return text

        display_weather = weather_label(weather_text)

        if display_weather == "晴れ":
            bg_color = "#fff4b6"
        elif display_weather == "曇り":
            bg_color = "#eeeeee"
        elif display_weather == "雨":
            bg_color = "#dbeafe"
        else:
            bg_color = "#eaf6ff"

        return {
            "weather": display_weather,
            "icon": get_icon(weather_text),
            "bg_color": bg_color,
            "max_temp": round(max_temp, 1),
            "min_temp": round(min_temp, 1),
            "humidity": forecast_list[0]["main"]["humidity"],
            "wind_speed": forecast_list[0]["wind"]["speed"],
            "forecast" :forecast,
            "daily_forecast":daily_forecast
        }

    except Exception as e:
        print("API error:", e)
        return {
            "weather": "取得失敗",
            "icon": "✖",
            "bg_color": "#eaf6ff",
            "max_temp": 0,
            "min_temp": 0,
            "humidity": 0,
            "wind_speed": 0
        }
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather_search():
    city = request.args.get("city")

    if not city:
        return render_template("index.html")
    city = CITY_MAP.get(city,city)
    weather_data = get_weather(city)
    today = datetime.now().strftime("%Y年%m月%d日")
    week = ["月", "火", "水", "木", "金", "土", "日"]
    today += f"（{week[datetime.now().weekday()]}）"
    save_weather(city, weather_data)

    return render_template(
        "weather.html",
        city=PREFECTURE_NAMES.get(city, city),
        weather=weather_data,
        today=today
    )


@app.route("/weather/<city>")
def weather(city):
    weather_data = get_weather(city)

    today = datetime.now().strftime("%Y年%m月%d日")
    week = ["月", "火", "水", "木", "金", "土", "日"]
    today += f"（{week[datetime.now().weekday()]}）"

    save_weather(city, weather_data)

    return render_template(
        "weather.html",
        city=PREFECTURE_NAMES.get(city, city),
        weather=weather_data,
        today=today
    )


@app.route("/hokkaido")
def hokkaido():
    return render_template("hokkaido.html")


@app.route("/tohoku")
def tohoku():
    return render_template("tohoku.html")


@app.route("/kanto")
def kanto():
    return render_template("kanto.html")


@app.route("/chubu")
def chubu():
    return render_template("chubu.html")


@app.route("/kinki")
def kinki():
    return render_template("kinki.html")


@app.route("/chugoku")
def chugoku():
    return render_template("chugoku.html")


@app.route("/shikoku")
def shikoku():
    return render_template("shikoku.html")


@app.route("/kyushu")
def kyushu():
    return render_template("kyushu.html")


@app.route("/history/<city>")
def history(city):
    rows = get_history(city)

    return render_template(
        "history.html",
        city=PREFECTURE_NAMES.get(city, city),
        rows=rows,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)